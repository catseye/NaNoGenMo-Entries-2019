#!/usr/bin/env python3.6

"""

*   input format: tokenstream
*   output format: tokenstream

Takes a stream of tokens and returns a new stream of tokens
where “ and ” are made to match up in each paragraph (or if
they cannot be made to match up, the paragraph is discarded.)

"""

import json
import re
import sys

import fsm


dialogue_state_machine = fsm.STATE_MACHINES['dialogue']


def check_double_quotes(paragraph):
    state = 'default'
    for word in paragraph:
        state = dialogue_state_machine(state, 0, word)
    if state == 'dialogue':
        raise ValueError("Missing close quote")


def rectify_paragraph(paragraph):
    try:
        check_double_quotes(paragraph)
        return True, paragraph
    except ValueError as e:
        error_message = str(e)
        if "Missing open quote" in error_message:
            return False, ['“'] + paragraph
        elif "Missing close quote" in error_message:
            return False, paragraph + ['”']
        else:
            return False, paragraph


def clean_quotes(paragraph):
    for i in (0, 1, 2):
        result, paragraph = rectify_paragraph(paragraph)
        if result:
            return paragraph
    sys.stderr.write("WARN: Couldn't fix paragraph, discarding: {}\n".format(' '.join(paragraph)))
    return []


def main(args):
    paragraphs = []
    paragraph = []

    for line in sys.stdin:
        word = line.strip()
        if word == "¶":
            paragraphs.append(paragraph)
            paragraph = []
        else:
            paragraph.append(word)

    for paragraph in paragraphs:
        for word in clean_quotes(paragraph):
            sys.stdout.write(word)
            sys.stdout.write("\n")
        sys.stdout.write("¶\n")


if __name__ == '__main__':
    main(sys.argv[1:])
