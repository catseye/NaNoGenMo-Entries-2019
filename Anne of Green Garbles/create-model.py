#!/usr/bin/env python3.6

"""

*   input format: tagged tokenstream
*   output format: Model JSON

Builds a Markov chain model given a (tagged) tokenstream.

"""

import json
import re
import sys


def main(argv):
    entries = {}
    last = None

    for line_no, line in enumerate(sys.stdin):
        components = line.strip().split(' ')
        word = components[-1]
        tags = ' '.join(sorted(components[:-1]))
        entry = '{} {}'.format(tags, word)
        if last is not None:
            m = entries.setdefault(last, {})
            m[entry] = m.get(entry, 0) + 1
        last = entry

    print(json.dumps(entries, sort_keys=True, indent=4))


if __name__ == '__main__':
    main(sys.argv)
