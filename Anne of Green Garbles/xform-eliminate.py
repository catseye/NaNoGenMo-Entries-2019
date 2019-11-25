#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

Removes certain tokens in the output tokenstream,
Notably [ and ], anything containing =, and
anything that's only digits.

"""


import re
import sys


def main(args):
    for line in sys.stdin:
        word = line.strip()
        if word in ('[', ']',):
            continue
        if '=' in word:
            continue
        if re.match(r'^\d*$', word):
            continue
        if word.isupper() and len(word) > 1:
            word = word.lower()
        sys.stdout.write('{}\n'.format(word))


if __name__ == '__main__':
    main(sys.argv[1:])
