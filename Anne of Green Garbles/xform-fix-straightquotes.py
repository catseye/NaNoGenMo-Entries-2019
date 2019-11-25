#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

Replaces straight quotes " with '“' and '”'.

("Straight quote" refers to straight double quotes.
Straight single quotes are called apostrophes and
are handled elsewhere.)

Not perfect, especially when '“' is omitted at the
beginning of the first paragraph of a chapter where
a word in all-caps or an illuminated letter stands in
its place.

"""

import re
import sys


def rectify_straightquotes(paragraph):
    """If the paragraph has an odd number of straight quotes, but starts
    with a straight quote, we assume a character's dialogue continues to
    the next paragraph, and we fix by adding a terminating straight quote."""
    count = sum([1 if w == '"' else 0 for w in paragraph])
    if (count % 2) == 1 and paragraph[0] == '"':
        return paragraph + ['"']
    else:
        return paragraph


def transform_paragraph(paragraph):
    paragraph = rectify_straightquotes(paragraph)
    accum = []
    count = 0
    for word in paragraph:
        if word == '"':
            if count % 2 == 0:
                word = '“'
            else:
                word = '”'
            count += 1
        accum.append(word)
    if count % 2 != 0:
        sys.stderr.write('*** Odd number of " found, discarding:\n\n{}\n\n'.format(' '.join(paragraph)))
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
            sys.stdout.write("{}\n".format(word))
        sys.stdout.write("¶\n")


if __name__ == '__main__':
    main(sys.argv[1:])
