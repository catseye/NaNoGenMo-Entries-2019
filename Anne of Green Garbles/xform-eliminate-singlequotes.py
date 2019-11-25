#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

Removes certain tokens in the output tokenstream,
notably ', as an alternative to handling single-quoting
properly.

"""


import re
import sys


def main(args):
    for line in sys.stdin:
        word = line.strip()
        if word in ("'", "‘", "’"):
            continue
        sys.stdout.write('{}\n'.format(word))


if __name__ == '__main__':
    main(sys.argv[1:])
