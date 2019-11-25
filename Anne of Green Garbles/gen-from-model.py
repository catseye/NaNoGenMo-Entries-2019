#!/usr/bin/env python3.6

"""

*   input format: Model JSON
*   output format: tagged tokenstream

Script to randomly walk a Markov chain model, generating a tagged tokenstream.

"""

from argparse import ArgumentParser
import json
from random import Random
import sys

OPTIONS = None


def pick_weighted_entry(freqmap, weight):
    acc = 0
    for key, value in freqmap.items():
        acc += value
        if acc >= weight:
            return key
            break
    raise KeyError


def gen_from_statemap(rgen, state, entry, entries):
    while True:
        freqmap = entries[entry]
        freq = sum(list(freqmap.values()))
        weight = rgen.randint(1, freq)
        entry = pick_weighted_entry(freqmap, weight)
        sys.stdout.write('{}\n'.format(entry))
        if entry.split(' ')[-1] == '¶':
            break
    return entry


def main(args):
    global OPTIONS

    argparser = ArgumentParser()
    argparser.add_argument('modelfile', metavar='FILENAME', type=str)
    argparser.add_argument("--title", type=str, default="Generated Novel")
    argparser.add_argument("--chapter-count", type=int)
    argparser.add_argument("--paragraph-count", type=int)
    argparser.add_argument("--state-machine", type=str, default='dialogue')
    argparser.add_argument("--random-seed", type=int, default=9009)
    OPTIONS = argparser.parse_args(args)

    rgen = Random()
    rgen.seed(OPTIONS.random_seed)

    with open(OPTIONS.modelfile, 'r') as f:
        entries = json.loads(f.read())

    for token in "# {} ¶".format(OPTIONS.title).split(' '):
        sys.stdout.write("{}\n".format(token))

    allowable_initial_entries = [k for k in entries.keys() if k.split(' ')[-1] == '¶']

    entry = rgen.choice(allowable_initial_entries)

    for chap_num in range(0, OPTIONS.chapter_count):
        for token in "### Chapter {} ¶".format(chap_num + 1).split(' '):
            sys.stdout.write("{}\n".format(token))
        p_count = OPTIONS.paragraph_count + rgen.randint(-2, 2)
        for para_num in range(0, p_count):
            entry = gen_from_statemap(rgen, 'default', entry, entries)


if __name__ == '__main__':
    main(sys.argv[1:])
