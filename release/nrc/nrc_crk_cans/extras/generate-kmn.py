#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright © 2019 Eddie Antonio Santos <Eddie.Santos@nrc-cnrc.gc.ca>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Generates the .kmn keyboard code for to make the touch layout work properly.
"""

import argparse
from collections import defaultdict

from libkeyboard.ioutils import setup_output
from libkeyboard.plains_cree_constants import COMBINING_CONSONANTS, VOWELS
from libkeyboard.syllabics import SYLLABICS


# The version number:
# Initial release is 1.0.0
name = "Plains Cree (Syllabics)"
version = f"1.0.0"


parser = argparse.ArgumentParser()
parser.add_argument("outfile", nargs="?")
parser.add_argument("--with-css", action="store_true", dest="css", default=False)
parser.add_argument("--without-css", action="store_false", dest="css")
args = parser.parse_args()
setup_output(args.outfile)

# Embedd CSS when --with-css is provided:
css_line = "store(&KMW_EMBEDCSS) 'nrc_crk_cans.css'".strip() if args.css else ""

# kwV -> set of ᑵᑷᑹᑻᑽᑿᒁ
prefix2syllabics = defaultdict(set)
for syllabic in SYLLABICS.values():
    prefix = syllabic.prefix
    if not prefix:
        continue
    prefix = prefix + 'V'
    prefix2syllabics[prefix].add(syllabic.cans)



print(
    f"""
c AUTOGENERATED FILE - DO NOT MODIFY!
store(&VERSION) '10.0'
store(&TARGETS) 'mobile'
store(&NAME) '{name}'
store(&COPYRIGHT) 'Copyright © 2019 National Research Council Canada'
store(&KEYBOARDVERSION) '{version}'
{css_line}
store(&LAYOUTFILE) 'nrc_crk_cans.keyman-touch-layout'
""".lstrip()
)

print("c These are used for backspace rules:")
for prefix, syllabics in prefix2syllabics.items():
    syllabics_list = ''.join(sorted(syllabics))
    print(f"store({prefix}) '{syllabics_list}'")

print(
    f"""
begin Unicode > use(main)
group(main) using keys
"""
)

# Generate rules that replace a final and a vowel with the composed syllabic
#    U+XXXX + [U_YYYY] > U+YYYY layer('default')
#   e.g. when [ ᐘ ] has been pressed following a ᐤ, insert ᐘ and switch to 'default' layer.
for sro, syllabic in SYLLABICS.items():
    if not sro.endswith((*VOWELS,)):
        continue
    if not sro.startswith((*COMBINING_CONSONANTS, "w")):
        continue

    final = SYLLABICS[sro[0]]
    keycode = syllabic.as_keycode
    composed_syllable = syllabic.as_character

    if len(sro) == 2:
        w = ""
        context = final.as_character
    else:
        assert len(sro) == 3 and sro[1] == "w"
        w = " ᐤ"
        context = f"{final.as_character} {SYLLABICS['w'].as_character}"

    print(f"  {context} + [{keycode}] > {composed_syllable} layer('default')", end=" ")
    print(f"c {final}{w} + [ {syllabic} ] > {syllabic}")

# Rules that decompose a syllable + backspace into its component consonants
print("  c Backspace rules: break apart a syllable on backspace")
for prefix in prefix2syllabics:
    consonants = prefix[:-1]
    consonant_chars = ' '.join(SYLLABICS[c].as_character for c in consonants)
    print(f"  any({prefix}) + [K_BKSP] > {consonant_chars} layer('{prefix}')")

# TODO: have some CHEESE lines that (disabled by default) handle FINAL + VOWEL
# and convert them to the appropriate syllabic to make up for the keyboard
# switching delay :/