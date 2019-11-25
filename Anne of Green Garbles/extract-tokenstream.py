#!/usr/bin/env python3.6

"""

*   input format: HTML
*   output format: tokenstream

Script that takes an HTML file and outputs a stream of tokens,
one per line (tokenstream).

Tries to ignore any element of the HTML which is not obviously
a paragraph of text (for example, ToC entries, chapter headings,
and Gutenberg license blocks.)

It retains punctuation symbols such as “ and ” and ( and ) and
. and , and ! and treats these as individual tokens.

It also produces ¶ symbols to indicate the end of each paragraph.

"""


import sys
import re
from bs4 import BeautifulSoup, NavigableString


def scan_token(s, tokens):
    s = s.lstrip()

    match = re.match(r'^(\w+)(.*?)$', s)
    if match:
        tokens.append(match.group(1))
        return match.group(2)

    match = re.match(r'^(.)(.*?)$', s)
    if match:
        tokens.append(match.group(1))
        return match.group(2)


def tokenize(s):
    tokens = []
    while s:
        s = scan_token(s, tokens)
    return tokens


def process_children(container):
    for child in container.children:
        if isinstance(child, NavigableString):
            continue

        if child.attrs.get('class') and 'toc' in child.attrs.get('class'):
            continue

        text = child.get_text().lstrip().replace('\n', ' ')
        if 'PROJECT GUTENBERG' in text.upper():
            continue
        if text.startswith(('CHAPTER', 'CONTENTS',)):
            continue

        if child.name.lower() in ('p',):
            tokens = tokenize(text)
            for token in tokens:
                print(token)
            print("¶")

        if child.name.lower() in ('div',):
            process_children(child)


def main(args):
    filename = args[0]
    with open(filename, 'rb') as f:
        text = f.read()
    soup = BeautifulSoup(text, 'html5lib')
    process_children(soup.body)


if __name__ == '__main__':
    main(sys.argv[1:])
