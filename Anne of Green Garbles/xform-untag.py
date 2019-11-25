#!/usr/bin/env python3.6

"""

*   input format: tagged tokenstream
*   output format: tokenstream

Takes a stream of tagged tokens and outputs a tokenstream with
all the tags stripped off.

"""

import re
import sys


def main(args):
    for line_no, line in enumerate(sys.stdin):
        entry = line.strip()
        word = entry.split(' ')[-1]
        sys.stdout.write('{}\n'.format(word))


if __name__ == '__main__':
    main(sys.argv[1:])
