#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

Takes a stream of tokens and returns a new stream of tokens
where freestanding `'` tokens are rewritten into apostrophes
when it looks like they should not have been freestanding.

This does not rewrite `'` into oriented single quotes.
It only leaves unoriented `'` at the beginning and end
of a paragraph.

Examples:

*   `don ' t` becomes `don't`

"""

import re
import sys

# 1. If the token on the right is one of these, we join it and the
# token on the left into a single contraction.  ("am" is for "ma'am")

RIGHTS = (
    't', 'm', 'd', 's', 'll', 've', 're', 'am',
)

# 2. If the token on the left is "o" or ends in "in" or "s" we attach
# the apostrophe to the left only, assume the right is a different word.
# This handles "plurals’" and "drinkin’" and "o’ course" and such.

# 3. Otherwise we attach  the apostrophe to the token on the right.
# This handles "’twas" and "’phone" and such.

# We don't pretend we can handle "’tweren’t".

def reduce_apostrophes(paragraph):
    accum = []
    i = 0
    while i < len(paragraph):
        word = paragraph[i]
        if word in ("'", "’",):
            if i == 0:
                pass
                # paragraph[i] = '‘'
            elif (i + 1) == len(paragraph):
                pass
                # paragraph[i] = '’'
            else:
                left = paragraph[i - 1]
                right = paragraph[i + 1]
                if right in RIGHTS:
                    paragraph[i - 1] = ''
                    paragraph[i + 1] = ''
                    paragraph[i] = '{}’{}'.format(left, right)
                elif left == 'o' or left.endswith(('in', 's',)) or not right[0].isalpha():
                    paragraph[i - 1] = ''
                    paragraph[i] = '{}’'.format(left)
                else:
                    paragraph[i + 1] = '’{}'.format(right)
                    paragraph[i] = ''
        i += 1

    return [word for word in paragraph if word]


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
        for word in reduce_apostrophes(paragraph):
            sys.stdout.write(word)
            sys.stdout.write("\n")
        sys.stdout.write("¶\n")


if __name__ == '__main__':
    main(sys.argv[1:])
