#!/usr/bin/env python3
# encoding: UTF-8

import random
import sys
import re
from bs4 import BeautifulSoup, NavigableString


def collapse_paragraph(t):
    for c in ('"', "'", '.', ',', '!', '?', ';', ':'):
        t = t.replace(c, '')
    for c in ('—'):
        t = t.replace(c, ' ')
    return ' '.join([u.upper() for u in t.split(' ')])


def paragraph_modification(t):
    if len([q for q in t if q == '"']) % 2 == 1:
        return None
    if t.endswith((':', '—"', 'swooned.')):
        return None
    if 'put in the wine' in t:
        return None

    words = collapse_paragraph(t)

    VERBED = (
        "SAID", "ASKED", "RAPPED", "LAUGHED", "REPLIED", "CONFESSED", "CRIED", "DEMANDED", "CONTINUED",
        "ADDED", "WHISPERED", "DIRECTED", "SUGGESTED", "HISSED", "MUTTERED", "RETURNED", "JERKED",
        "PRONOUNCED", "EXPLAINED", "GROANED",
    )

    I_SAID = ["I " + verb for verb in VERBED]
    for h in I_SAID:
        if h in words:
            return 'I adjusted my rainbow-coloured novelty wig.'

    SHE_SAID = (
        ["SHE " + verb for verb in VERBED]
    )
    for h in SHE_SAID:
        if h in words:
            return 'She adjusted her rainbow-coloured novelty wig.'

    HE_SAID = (
        ["HE " + verb for verb in VERBED] +
        ["SMITH " + verb for verb in VERBED] +
        [verb + " SMITH" for verb in VERBED] +
        [verb + " MY FRIEND" for verb in VERBED] +
        ["FU-MANCHU " + verb for verb in VERBED] +
        [verb + " FU-MANCHU" for verb in VERBED] +
        ["WEYMOUTH " + verb for verb in VERBED] +
        [verb + " WEYMOUTH" for verb in VERBED] +
        ["THE DETECTIVE " + verb for verb in VERBED] +
        [verb + " THE DETECTIVE" for verb in VERBED] +
        []
    )
    for h in HE_SAID:
        if h in words:
            return 'He adjusted his rainbow-coloured novelty wig.'

    return None


def main(args):
    filename = args[0]
    lines = []
    accum = False
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip()
            if line == '<A NAME="chap01"></A>':
                accum = True
            if accum:
                lines.append(line)
    text = (
        '<!DOCTYPE html><html><head><title>The Insidiously Rainbow-Wigged Dr. Fu-Manchu</title></head><body>' +
        '<h1>The Insiduously Rainbow-Wigged Dr. Fu-Manchu</h1>' +
        '\n'.join(lines) +
        '</body></html>'
    )
    soup = BeautifulSoup(text, 'html.parser')

    history = [(-1, "zzz")]
    p_num = 0
    for child in soup.body.children:
        if isinstance(child, NavigableString):
            continue
        if 'The Project Gutenberg EBook' in child.get_text():
            continue
        if 'End of Project Gutenberg' in child.get_text():
            continue
        paragraph_text = child.get_text().strip()
        paragraph_text = paragraph_text.replace("fashionable hat", "fashionable hairpiece")
        if child.name.lower() == 'p':
            p_num += 1

            modification = paragraph_modification(paragraph_text)
            if modification is not None:
                (last_p_num, last_modification) = history[-1]

                if last_modification != modification and (p_num - last_p_num > 1):
                    history.append((p_num, modification))
                    paragraph_text += '  ' + modification

        paragraph_text = "<{}>{}</{}>".format(child.name, paragraph_text, child.name)
        print(paragraph_text)
    print('</html>')


if __name__ == '__main__':
    main(sys.argv[1:])
