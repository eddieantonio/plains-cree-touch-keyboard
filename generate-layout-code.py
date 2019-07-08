#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Generates the .kmn keyboard code for to make the touch layout work properly.
"""

from syllabics import SYLLABICS
from plains_cree_constants import COMBINING_CONSONANTS


PREAMBLE = """
store(&VERSION) '10.0'
store(&TARGETS) 'iphone androidphone mobile'
store(&NAME) 'Plains Cree Syllabics Keyboard'
store(&COPYRIGHT) 'Copyright © 2019 National Research Council Canada'
store(&EthnologueCode) 'crk'
store(&KEYBOARDVERSION) '0.1.0'
store(&LAYOUTFILE) 'nrc_cr_cans.keyman-touch-layout'

c TODO: Embed custom CSS?

begin Unicode > use(main)
group(main) using keys
""".lstrip()


def as_keycode(syllabic):
    return f'[U_{syllabic.scalar_value:04X}]'


def as_codepoint(syllabic):
    return f'U+{syllabic.scalar_value:04X}]'


print(PREAMBLE)

for consonant in COMBINING_CONSONANTS:
    final = SYLLABICS[consonant]
    print("  +", as_keycode(final), ">", as_codepoint(final), f"layer('{consonant}V)'")
