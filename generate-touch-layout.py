#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright © 2019 Eddie Antonio Santos <Eddie.Santos@nrc-cnrc.gc.ca>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import re
import sys
from ioutils import setup_output
from plains_cree_constants import COMBINING_CONSONANTS, VOWELS
from syllabics import SYLLABICS


# For guidelines on how to create a comfortable layout, I used two sources of
# data:
#
#  - I counted unigrams, bigrams, and syllabics [Santos n.d.] from the
#    Ahenekew-Wolfart corpus [Arppe n.d.]
#  - I consulted [Park 2008] and choose placements based on  a 7mm layout, as
#    this will fit on modern smartphones.
#
# I placed vowels first, on the right-side, placing the most common vowels in
# the most subjectively comfortable positions, and where the error rate and
# time to press rates were "good", all according to [Park 2008]. This is
# intended to maximize the comfort of typing a vowel from using your right
# thumb. I placed "special" consonants---"h", "w"---in the remaining "good" spots
# on the right-side of the keyboard. I placed "r" in the uncomfortable spot on
# the right-side of the keyboard, as "r" is rarely used. Importantly, the most
# common vowels were placed on the third column from the right, which [Park
# 2008] claims to fit to the natural axis of rotation of the thumb.
#
# To place the remaining consonants, I mirrored the 7mm "goodness" charts from
# [Park 2008] and repeated the process, placing the most common consonants in
# comfortable positions. The third column from the left contains the most
# often used consonants, excluding the "special" consonants "h" and "w". "l"
# is placed in the uncomfortable spot on the left side of the keyboard.
#
# This is my rationale, yet the final positioning is ultimately quite
# arbitrary. I tried to place keys that "go together well" besides each other,
# like the the nasals ("m", and "n") are besides each other; the glides ("y",
# "w") are besides each other. I've tried to make short vowels and their long
# equivilents next to each other. I was successfull for "a"/"â" and "i"/î",
# but for sake of comfort and frequency, I split up "ô" from "o".
#
# [Arppe n.d.]: http://altlab.artsrn.ualberta.ca/wp-content/uploads/2019/05/Arppe_et_al_PAC49.pdf
# [Park 2008]: https://www.sciencedirect.com/science/article/pii/S0169814109001036
# [Santos n.d.]: https://gist.github.com/eddieantonio/1b0f25f1c6d78e6dfb611f490a0822c7#file-unigrams-tsv
LAYOUT = """
[  hk ] [  m   ] [ n ] [ y ] [ w ] [ i ] [ î ] [  ô ]
[  l  ] [  p   ] [ t ] [ s ] [ â ] [ a ] [ o ] [  r ]
[ ABC ] [  c   ] [ k ] [  NNBSP  ] [ ê ] [ h ] [ BS ]
[ 123 ] [ MENU ] [         SP          ] [ . ] [ CR ]
"""

# Keyman defines each key's width as being 100 units.
# The default padding is 5 units.
SLOT_WIDTH = 105  # How much width each "slot" occupies
PADDING_BETWEEN = 5  # How much of the slot is just the padding.
KEY_WIDTH = SLOT_WIDTH - PADDING_BETWEEN  # How much of the slot is the key itself

# Key types
# https://help.keyman.com/developer/10.0/guides/develop/creating-a-touch-keyboard-layout-for-amharic-the-nitty-gritty#id488808
NORMAL_KEY = "0"
SPECIAL_KEY = "1"  # for ABC, 123, Enter, BS, etc.
ACTIVE_KEY = "2"  # for non-default vowel syllabics
DEAD_KEY = "8"  # for active consonant/w.
BLANK_KEY = "9"  # placeholder for missing nwV syllabics

ALWAYS_RETURN_TO_DEFAULT_LAYER = {"hk", "l", "r", "h"}


class Key:
    """
    Represents a generic key on the keyboard.
    """

    def __init__(self, label):
        self.label = label

    @classmethod
    def label_matches(cls, tag):
        return True

    @property
    def extra_attributes(self):
        if self.label in ALWAYS_RETURN_TO_DEFAULT_LAYER:
            return {"nextlayer": "default"}
        return {}

    def dictionary_for_key(self):
        syllabic = SYLLABICS[self.label]
        return dict(
            id=syllabic.key_code,
            text=syllabic.cans,
            **self.extra_attributes,
        )

    def dictionary_for_key_with_mode(self, mode, consonant):
        assert mode in ("CV", "CwV")
        return self.dictionary_for_key()

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}({self.label!r})"



class VowelKey(Key):
    """
    Represents a key on the keyboard for a vowel.

    Vowel keys change after a consonant has been pressed or after a consonant
    and a 'w' has been pressed.
    """

    @classmethod
    def label_matches(cls, tag):
        return tag in VOWELS

    def dictionary_for_key_with_mode(self, mode, consonant):
        sro = mode.replace("C", consonant).replace("V", self.label)
        try:
            syllabic = SYLLABICS[sro]
        except KeyError:
            # nwV exceptional cases. Place a blank here instead.
            assert sro.startswith("nw")
            return dict(
                id="",  # A blank code is valid, apparently?
                sp=BLANK_KEY,
                text="",
            )
        else:
            result = dict(
                id=syllabic.key_code,
                text=syllabic.cans,
                nextlayer="default",
            )
            # Highlight the vowels that have changed.
            if consonant:
                result.update(sp=ACTIVE_KEY)
            return result


class PeriodKey(Key):
    """
    The period key, which has a pop-up for additional punctuation.
    """

    @classmethod
    def label_matches(cls, tag):
        return tag == "."

    def dictionary_for_key(self):
        return {
            "id": "U_166E",
            "text": "᙮",
            "sk": [
                {"text": ",", "id": "U_002C"},
                {"text": "?", "id": "U_003F"},
                {"text": "!", "id": "U_0021"},
            ],
            "nextlayer": "default",
        }


class SpecialKey(Key):
    """
    Any key that has special semantics.
    """

    SETTINGS = {
        "SP": dict(id="K_SPACE", text="", width=4, nextlayer="default", sp=NORMAL_KEY),
        "BS": dict(id="K_BKSP", text="*BkSp*", nextlayer="default", sp=SPECIAL_KEY),
        "123": dict(id="K_NUMLOCK", text="*123*", nextlayer="default", sp=SPECIAL_KEY),
        "NNBSP": dict(
            id="U_202F", text="", width=2, nextlayer="default", sp=NORMAL_KEY
        ),
        "ABC": dict(
            id="K_UPPER", text="*ABC*", nextlayer="default", sp=SPECIAL_KEY
        ),  # TODO: make a latin layout
        "CR": dict(id="K_ENTER", text="*Enter*", nextlayer="default", sp=SPECIAL_KEY),
        "MENU": dict(id="K_LOPT", text="*Menu*", nextlayer="default", sp=SPECIAL_KEY),
    }

    def dictionary_for_key(self):
        settings = self.SETTINGS[self.label]
        key = dict(
            id=settings["id"],
            text=settings["text"],
            sp=settings["sp"],
            nextlayer=settings["nextlayer"],
        )
        if self.proportional_width > 1:
            key.update(width=self.effective_width)
        return key

    @property
    def proportional_width(self):
        return self.SETTINGS[self.label].get("width", 1)

    @classmethod
    def label_matches(cls, tag):
        return tag in cls.SETTINGS

    @property
    def effective_width(self):
        """
        The width of the key taking the proportional width and default padding
        into account.

        This EXCLUDES the current key's padding.
        """
        padding = (self.proportional_width - 1) * PADDING_BETWEEN
        return self.proportional_width * KEY_WIDTH + padding


class CombiningConsonantKey(Key):
    """
    A consonant key that places the touch keyboard into a CV layer.
    """

    @classmethod
    def label_matches(cls, tag):
        return tag in COMBINING_CONSONANTS

    @property
    def consonant(self):
        return self.label[0]

    def dictionary_for_key_with_mode(self, mode, consonant):
        # Act like a normal key...
        obj = super().dictionary_for_key()
        # Except switch to the consonant layer when needed
        obj.update(nextlayer=self.consonant + "V")
        # If we're already in that layer, then hightlight this consonant
        if consonant == self.consonant:
            obj.update(sp=DEAD_KEY)
        return obj


class WKey(CombiningConsonantKey):
    """
    The W key. When in the 'default' layer, this acts like a regular
    combining consonant.

    However, when in a CV layer, this goes into a CwV layer.
    """

    @classmethod
    def label_matches(cls, tag):
        return tag == "w"

    @property
    def consonant(self):
        return "w"

    def dictionary_for_key_with_mode(self, mode, consonant):
        obj = super().dictionary_for_key()
        if not consonant and mode == "CV":
            # Pressed 'w' key in default layout.
            # This means we want to enter wV syllables.
            obj.update(nextlayer=f"wV")
        elif mode == "CV":
            # Assume we have pressed a consonant. Continue to CwV layer.
            obj.update(nextlayer=f"{consonant}wV")
        elif mode == "CwV":
            # ¯\_(ツ)_/¯
            obj.update(nextlayer=f"default", sp=DEAD_KEY)

        return obj


def parse_ascii_layout(layout: str) -> list:
    """
    Parses the ASCII art keyboard into a list of rows, each row containing a
    Key.
    """
    raw_rows = layout.strip().split("\n")
    keyboard = []
    for raw_keys in raw_rows:
        row = []
        for match in re.finditer(r"""\[\s*(\S+)\s*\]""", raw_keys):
            label = match.group(1)
            for cls in (
                WKey,
                CombiningConsonantKey,
                VowelKey,
                PeriodKey,
                SpecialKey,
                Key,
            ):
                if cls.label_matches(label):
                    break
            key = cls(label)
            row.append(key)
        keyboard.append(row)
    return keyboard


def create_keyman_touch_layout_json(keyboard: list) -> dict:
    """
    Returns a JSON-serializable dictionary that describes a touch-layout for
    phones in the format that KeymanWeb requires.
    """
    layers = []
    for consonant in ("", *COMBINING_CONSONANTS):
        # Generate a layer for either CV or CwV combinations
        for mode in ("CV", "CwV"):
            # What is the name of this layer?
            if consonant == "" and mode == "CV":
                layer_id = "default"
            else:
                layer_id = mode.replace("C", consonant)

            layout_rows = []
            for rowid, row in enumerate(keyboard, start=1):
                # Generate the keys for this row!
                keys = [
                    key.dictionary_for_key_with_mode(mode, consonant) for key in row
                ]

                # TODO: add on to this pile of hacks...
                # only give a width and padding for nnbsp and space keys :/
                # So apparently, key width is supposed to add up to 100 * number of keys..
                # when the key is greater than 100, you have to add padding (default 5)

                # Post-process the keys:
                # Implement workarounds to make the layout render correctly
                for index, key in enumerate(keys):
                    # Bug 🐛 in KeymanWeb: width and pad MUST be strings 🙃
                    # https://github.com/keymanapp/keyman/issues/119
                    if "width" in key:
                        key["width"] = str(key["width"])
                    if "pad" in key:
                        key["pad"] = str(PADDING_BETWEEN)

                layout_rows.append({"id": rowid, "key": keys})

            layers.append(dict(id=layer_id, row=layout_rows))

    phone_layout = {"font": "Euphemia", "layer": layers, "displayUnderlying": False}
    return {"phone": phone_layout}


#################################### Main ####################################
if __name__ == "__main__":
    # Setup output, either to stdout or
    setup_output()

    # Parse the table of syllabics, as well as the keyboard layout.
    keyboard = parse_ascii_layout(LAYOUT)

    layout = create_keyman_touch_layout_json(keyboard)
    json.dump(layout, sys.stdout, indent=2, ensure_ascii=False)
    print()
