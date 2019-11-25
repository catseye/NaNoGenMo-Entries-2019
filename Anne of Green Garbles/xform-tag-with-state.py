#!/usr/bin/env python3.6

"""

*   input format: tagged tokenstream
*   output format: tagged tokenstream

Takes a stream of tokens and outputs a tokenstream where every
token is decorated with what the new state of the state machine
would be after accepting the token.

As a side effect it checks if the structure is
consistent (a prerequisite for creating a stateful stochastic
model)

"""

from argparse import ArgumentParser
import re
import sys

import fsm

OPTIONS = None


def parse_entry(entry):
    components = entry.strip().split(' ')
    return components[-1], dict([pair.split('=') for pair in components[:-1]])


def format_entry(word, tags):
    return '{} {}'.format(' '.join(sorted('{}={}'.format(k, v) for k, v in tags.items())), word)


def main(args):
    global OPTIONS

    argparser = ArgumentParser()
    argparser.add_argument("--state-machine", type=str, default='dialogue')
    OPTIONS = argparser.parse_args(args)

    state = 'default'
    advance_state_machine = fsm.STATE_MACHINES[OPTIONS.state_machine]

    for line_no, line in enumerate(sys.stdin):
        word, tags = parse_entry(line)
        state = advance_state_machine(state, line_no, word)
        tags['state'] = state
        entry = format_entry(word, tags)
        sys.stdout.write('{}\n'.format(entry))


if __name__ == '__main__':
    main(sys.argv[1:])
