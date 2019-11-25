#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

If the last word before a ¶ is alphabetic,
insert a full stop.

"""


import re
import sys


def main(args):
    last_is_alpha = False
    for line in sys.stdin:
        word = line.strip()
        if word in ('¶',) and last_is_alpha:
            sys.stdout.write('.\n')
        sys.stdout.write('{}\n'.format(word))
        last_is_alpha = word[0].isalpha()


if __name__ == '__main__':
    main(sys.argv[1:])
