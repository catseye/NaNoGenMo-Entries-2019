#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

Takes a stream of tokens and returns a new stream of tokens
where freestanding `.` tokens are rewritten when it looks
like they should not have been freestanding.

Examples:

*   `Mrs . Derrigan` becomes `Mrs. Derrigan`
*   `J . Pierpoint Flathead` becomes `J. Pierpoint Flathead`

"""

import re
import sys


def is_abbreviation(word):
    if word.isupper() and len(word) == 1:
        return True
    if word in ('Mrs', 'Mr', 'Dr', 'Ms'):
        return True
    return False


def reduce_fullstops(paragraph):
    accum = []
    for word in paragraph:
        if word == '.' and accum and is_abbreviation(accum[-1]):
            accum[-1] = accum[-1] + '.'
        else:
            accum.append(word)
    return accum


def main(args):
    paragraphs = []
    paragraph = []

    for line in sys.stdin:
        word = line.strip()
        if word == "¶":
            paragraphs.append(paragraph)
            paragraph = []
        else:
            paragraph.append(word)

    for paragraph in paragraphs:
        for word in reduce_fullstops(paragraph):
            sys.stdout.write(word)
            sys.stdout.write("\n")
        sys.stdout.write("¶\n")


if __name__ == '__main__':
    main(sys.argv[1:])
