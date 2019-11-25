#!/usr/bin/env python3.6

"""

Script to orchestrate building.

"""

from argparse import ArgumentParser
import sys
import os
from subprocess import run


OPTIONS = None


def zrun(targ, command, **kwargs):
    if targ is not None:
        targ = targ.format(**kwargs)
        if os.path.exists(targ):
            return
    command += ' 2>>{bucket}/stderr.log'
    c = command.format(**kwargs)
    sys.stderr.write("*** {}\n".format(c))
    run(c, shell=True, check=True)


def process_pipeline(bucket, random_seed):
    try:
        os.mkdir(bucket)
    except FileExistsError:
        pass

    context = dict(
        bucket=bucket,
    )
    zrun(None, 'rm -f {bucket}/stderr.log', **context)
    if OPTIONS.clean_gen:
        zrun(None, 'rm -f {bucket}/out1.txt {bucket}/out2.txt {bucket}/novel.md {bucket}/novel.html', **context)

    instances = []
    for num, filename in enumerate(OPTIONS.filenames):
        print(filename)
        context = dict(
            filename=filename,
            bucket=bucket,
            num=str(num),
            fsm=OPTIONS.state_machine,
        )
        zrun('{bucket}/tokens_{num}_raw.txt', './extract-tokenstream.py "{filename}" > {bucket}/tokens_{num}_raw.txt', **context)
        zrun('{bucket}/tokens_{num}_elim.txt', './xform-eliminate.py "{filename}" < {bucket}/tokens_{num}_raw.txt > {bucket}/tokens_{num}_elim.txt', **context)
        zrun('{bucket}/tokens_{num}_deduped.txt', './xform-dedup.py < {bucket}/tokens_{num}_elim.txt > {bucket}/tokens_{num}_deduped.txt', **context)
        zrun('{bucket}/tokens_{num}_sentences.txt', './xform-fix-fullstops.py < {bucket}/tokens_{num}_deduped.txt > {bucket}/tokens_{num}_sentences.txt', **context)
        zrun('{bucket}/tokens_{num}_capitalized.txt', './xform-fix-capitalization.py < {bucket}/tokens_{num}_sentences.txt > {bucket}/tokens_{num}_capitalized.txt', **context)
        zrun('{bucket}/tokens_{num}_end-punctuation.txt', './xform-fix-end-punctuation.py < {bucket}/tokens_{num}_capitalized.txt > {bucket}/tokens_{num}_end-punctuation.txt', **context)
        zrun('{bucket}/tokens_{num}_contractions.txt', './xform-fix-apostrophes.py < {bucket}/tokens_{num}_end-punctuation.txt > {bucket}/tokens_{num}_contractions.txt', **context)
        zrun('{bucket}/tokens_{num}_singlequotes.txt', './xform-eliminate-singlequotes.py < {bucket}/tokens_{num}_contractions.txt > {bucket}/tokens_{num}_singlequotes.txt', **context)
        zrun('{bucket}/tokens_{num}_straightquotes.txt', './xform-fix-straightquotes.py < {bucket}/tokens_{num}_singlequotes.txt > {bucket}/tokens_{num}_straightquotes.txt', **context)
        zrun('{bucket}/tokens_{num}_clean.txt', './xform-fix-doublequotes.py < {bucket}/tokens_{num}_straightquotes.txt > {bucket}/tokens_{num}_clean.txt', **context)
        if OPTIONS.markov_order == 2:
            zrun('{bucket}/tokens_{num}_prev1_tagged.txt', './xform-tag-with-prev-tokens.py < {bucket}/tokens_{num}_clean.txt > {bucket}/tokens_{num}_prev1_tagged.txt', **context)
        elif OPTIONS.markov_order == 1:
            zrun('{bucket}/tokens_{num}_prev1_tagged.txt', 'cat < {bucket}/tokens_{num}_clean.txt > {bucket}/tokens_{num}_prev1_tagged.txt', **context)
        else:
            raise NotImplementedError(OPTIONS.markov_order)
        zrun('{bucket}/tokens_{num}_state_tagged.txt', './xform-tag-with-state.py --state-machine={fsm} < {bucket}/tokens_{num}_prev1_tagged.txt > {bucket}/tokens_{num}_state_tagged.txt', **context)
        instances.append(num)

    context = dict(
        bucket=bucket,
        instreams=' '.join(['{bucket}/tokens_{i}_state_tagged.txt'.format(bucket=bucket, i=i) for i in instances]),
        random_seed=str(random_seed),
        fsm=OPTIONS.state_machine,
        title=OPTIONS.title,
    )
    zrun('{bucket}/model.json', 'cat {instreams} | ./create-model.py > {bucket}/model.json', **context)
    zrun('{bucket}/out1.txt', './gen-from-model.py --chapter-count=30 --paragraph-count=35 --title="{title}" --random-seed={random_seed} --state-machine={fsm} {bucket}/model.json > {bucket}/out1.txt', **context)
    zrun('{bucket}/out2.txt', './xform-untag.py < {bucket}/out1.txt > {bucket}/out2.txt', **context)
    zrun('{bucket}/out3.txt', './xform-remove-short-sentences.py < {bucket}/out2.txt > {bucket}/out3.txt', **context)
    zrun('{bucket}/novel.md', './render-markdown.py < {bucket}/out2.txt > {bucket}/novel.md', **context)
    zrun(None, 'wc -w {bucket}/novel.md', **context)
    zrun('{bucket}/novel.html', 'markdown_py < {bucket}/novel.md > {bucket}/novel.html', **context)
    zrun(None, 'firefox {bucket}/novel.html &', **context)


def main(args):
    global OPTIONS

    argparser = ArgumentParser()
    argparser.add_argument('dirname', metavar='DIRNAME', type=str)
    argparser.add_argument('filenames', metavar='FILENAME', type=str, nargs='+')

    argparser.add_argument("--title", type=str, default="Generated Novel")
    argparser.add_argument("--state-machine", type=str, default='dialogue')
    argparser.add_argument("--random-seed", type=str, default='9009')
    argparser.add_argument("--clean-gen", action='store_true')
    argparser.add_argument("--markov-order", type=int, default=1)

    OPTIONS = argparser.parse_args(args)

    if OPTIONS.random_seed == 'random':
        import random
        random_seed = random.randint(0, 1000000)
        sys.stderr.write(">>> Random seed is: {}".format(random_seed))
    else:
        random_seed = int(OPTIONS.random_seed)

    process_pipeline(OPTIONS.dirname, random_seed)


if __name__ == '__main__':
    main(sys.argv[1:])
