#!/usr/bin/env python3.6

"""

*   input format: tagged tokenstream
*   output format: tagged tokenstream

Takes a stream of tagged tokens and outputs a tokenstream with
the prev1 tag stripped off.

"""

import re
import sys


def parse_entry(entry):
    components = entry.strip().split(' ')
    return components[-1], dict([pair.split('=') for pair in components[:-1]])


def format_entry(word, tags):
    return '{} {}'.format(' '.join(sorted('{}={}'.format(k, v) for k, v in tags.items())), word)


def main(args):
    for line_no, line in enumerate(sys.stdin):
        word, tags = parse_entry(line)
        if 'prev1' in tags:
            del tags['prev1']
        sys.stdout.write('{}\n'.format(format_entry(word, tags)))


if __name__ == '__main__':
    main(sys.argv[1:])
