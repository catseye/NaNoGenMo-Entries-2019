🙚 The Insidiously Rainbow-Wigged Dr. Fu-Manchu 🙘
================================================

_The moment I opened the dust-covered tome I could feel the noxious
waves of Orientalism oozing out from it.  Whither the antidote?
I racked my brains for anything that might prove effective, but
precious time was slipping by!  I had to pick something, and fast.
There was no more that I could do but to try it and hope..._

To build
--------

Generated using Python 3.5.2 and Beautiful Soup 4.6.3, then converted from
HTML to Markdown using Pandoc 1.16.0.2.

    pip install beautifulsoup4
    wget https://www.gutenberg.org/files/173/173-h/173-h.htm
    ./tirwdfm.py 173-h.htm > "generated/The Insidiously Rainbow-Wigged Dr. Fu-Manchu.html"
    pandoc --from=html --to=markdown < "generated/The Insidiously Rainbow-Wigged Dr. Fu-Manchu.html" \
                                     > "generated/The Insidiously Rainbow-Wigged Dr. Fu-Manchu.md"
