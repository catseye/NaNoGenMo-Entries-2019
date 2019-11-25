#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

Takes a stream of tokens and returns a new stream of tokens
where freestanding `'` tokens are rewritten into oriented single
quotes, if they look like they could be such.  Assumes
contractions (apostrophes) have already been taken care of.

NOTE: not used in current novel generation pipeline.

"""

import re
import sys


def transform_paragraph(paragraph):
    accum = []
    count = 0
    for word in paragraph:
        if word == "'":
            if count % 2 == 0:
                word = "‘"
            else:
                word = '’'
            count += 1
        accum.append(word)
    if count % 2 != 0:
        sys.stderr.write("*** Odd number of ' found, discarding:\n\n{}\n\n".format(' '.join(paragraph)))
        return []
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
        for word in transform_paragraph(paragraph):
            sys.stdout.write(word)
            sys.stdout.write("\n")
        sys.stdout.write("¶\n")


if __name__ == '__main__':
    main(sys.argv[1:])
