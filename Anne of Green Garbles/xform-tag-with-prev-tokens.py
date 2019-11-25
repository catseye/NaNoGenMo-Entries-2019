#!/usr/bin/env python3.6

"""

*   input format: tagged tokenstream
*   output format: tagged tokenstream

Takes a stream of tagged tokens and outputs a tagged tokenstream where
every token is given a new tag, prev1, which contains the token preceding
it.

Can be used to make an order-2 Markov chain.

"""

import re
import sys


def parse_entry(entry):
    components = entry.strip().split(' ')
    return components[-1], dict([pair.split('=') for pair in components[:-1]])


def format_entry(word, tags):
    return '{} {}'.format(' '.join(sorted('{}={}'.format(k, v) for k, v in tags.items())), word)


def main(args):
    last = "¶"

    for line_no, line in enumerate(sys.stdin):
        word, tags = parse_entry(line)
        tags['prev1'] = last
        entry = format_entry(word, tags)
        sys.stdout.write('{}\n'.format(entry))
        last = word


if __name__ == '__main__':
    main(sys.argv[1:])
