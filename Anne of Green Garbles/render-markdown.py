#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: Markdown

Takes a stream of tokens and outputs it in a more human-readable
fashion as paragraphs of Markdown.

"""

import re
import sys


def render_paragraph(paragraph):
    a = ''
    last = None
    for word in paragraph:

        # transform word
        if word[0].isalpha() and last in ('“', '.',):
            word = word.capitalize()

        # account for space (or not) before word
        if last is None:
            a += word
            last = word
            continue
        if last in ('“', '(',):
            a += word
            last = word
            continue
        if word in ('”', ')',):
            a += word
            last = word
            continue
        if word in (',', ';', ':', '.', '.', '?', '!', '—', '-', '’') and (last[-1].isalpha() or last in (')', '”')):
            a += word
            last = word
            continue
        if word[0].isalpha() and last in ('—', '-', '’',):
            # NOTE: '’' should probably not be allowable in this case, if reduce-apostrophes was used and worked.
            a += word
            last = word
            continue
        a += ' ' + word
        last = word
    return a


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
        sys.stdout.write(render_paragraph(paragraph))
        sys.stdout.write("\n\n")


if __name__ == '__main__':
    main(sys.argv[1:])
