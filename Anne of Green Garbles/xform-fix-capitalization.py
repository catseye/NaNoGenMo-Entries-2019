#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

Capitalize first word after a ¶.

"""


import re
import sys


def main(args):
    at_start = True
    for line in sys.stdin:
        word = line.strip()
        if word in ('¶',):
            at_start = True
        if at_start and word[0].isalpha():
            word = word.capitalize()
            at_start = False
        sys.stdout.write('{}\n'.format(word))


if __name__ == '__main__':
    main(sys.argv[1:])
