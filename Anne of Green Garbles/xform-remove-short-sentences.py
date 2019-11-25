#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

Takes a stream of tokens and returns a new stream of tokens
with short sentences removed.

A short sentence is a sequence of tokens following a
"." or a "¶" which contains one or two alphanumeric
tokens, and no quotation marks, and none of the following:
`#` `##` `###`

"""

import re
import sys


def sentences(paragraph):
    them = []
    accum = []
    for word in paragraph:
        accum.append(word)
        if word == '.':
            them.append(accum)
            accum = []
    if accum:
        them.append(accum)
        accum = []
    return them


def sentence_is_short(sentence):
    count = 0
    for word in sentence:
        if word in ('“', '”', '#', '##', '###',):
            return False
        if word[0].isalpha():
            count += 1
    return count < 3


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
        for sentence in sentences(paragraph):
            if sentence_is_short(sentence):
                #sys.stderr.write('*** SHORT: {}\n'.format(' '.join(sentence)))
                pass
            else:
                for word in sentence:
                    sys.stdout.write(word)
                    sys.stdout.write("\n")
        sys.stdout.write("¶\n")


if __name__ == '__main__':
    main(sys.argv[1:])
