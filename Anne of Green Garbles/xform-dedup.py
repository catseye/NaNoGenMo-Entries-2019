#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

Replaces multiple occurrences of certain tokens with
a single occurrence of that token.  Notably ¶.

"""


import re
import sys


def main(args):
    last = None
    for line in sys.stdin:
        word = line.strip()
        if word == last:
            if word in ('¶', '.', '-',):
                continue
        sys.stdout.write('{}\n'.format(word))
        last = word


if __name__ == '__main__':
    main(sys.argv[1:])
