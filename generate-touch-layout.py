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


LAYOUT = """
[  s  ] [  w   ] [ m ] [ l ] [ r ] [ â ] [ i ] [  î ]
[  hk ] [  t   ] [ k ] [ h ] [ p ] [ a ] [ o ] [  c ]
[ ABC ] [  y   ] [ n ] [  NNBSP  ] [ ê ] [ ô ] [ BS ]
[ 123 ] [ MENU ] [         SP          ] [ . ] [ CR ]
"""

# For some reason, I decided each "slot" would be 15 units
# There are 8 keys, giving a total width of 8 ⨉ 15 = 120 units.
SLOT_WIDTH = 15  # How much width each "slot" occupies
PADDING_BETWEEN = 2  # How much of the slot is just the padding.
KEY_WIDTH = SLOT_WIDTH - PADDING_BETWEEN  # How much of the slot is the key itself

# Key types
# https://help.keyman.com/developer/10.0/guides/develop/creating-a-touch-keyboard-layout-for-amharic-the-nitty-gritty#id488808
NORMAL_KEY = "0"
SPECIAL_KEY = "1"  # TODO: for vowels?
ACTIVE_KEY = "2"  # TODO: for active consonant?
BLANK_KEY = "9"

ALWAYS_RETURN_TO_DEFAULT_LAYER = {"hk", "l", "r", "h"}


class Key:
    """
    Represents a generic key on the keyboard.
    """

    proportional_width = 1

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
            width=self.effective_width,
            **self.extra_attributes,
        )

    def dictionary_for_key_with_mode(self, mode, consonant):
        assert mode in ("CV", "CwV")
        return self.dictionary_for_key()

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}({self.label!r})"

    @property
    def effective_width(self):
        """
        The width of the key taking the proportional width and default padding
        into account.

        This EXCLUDES the current key's padding.
        """
        padding = (self.proportional_width - 1) * PADDING_BETWEEN
        return self.proportional_width * KEY_WIDTH + padding


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
                width=self.effective_width,
            )
        else:
            return dict(
                id=syllabic.key_code,
                text=syllabic.cans,
                nextlayer="default",
                width=self.effective_width,
            )


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
            "width": self.effective_width,
            "sk": [{"text": "!", "id": "U_0021"}, {"text": "?", "id": "U_0022"}],
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
        return dict(
            id=settings["id"],
            text=settings["text"],
            width=self.effective_width,
            sp=settings["sp"],
            nextlayer=settings["nextlayer"],
        )

    @property
    def proportional_width(self):
        return self.SETTINGS[self.label].get("width", 1)

    @classmethod
    def label_matches(cls, tag):
        return tag in cls.SETTINGS


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

    def dictionary_for_key(self):
        obj = super().dictionary_for_key()
        obj.update(nextlayer=self.consonant + "V")
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
            obj.update(nextlayer=f"default")

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

                # Post-process the keys:
                # Implement workarounds to make the layout render correctly
                for index, key in enumerate(keys):
                    assert "width" in key, "A key is missing its width property"
                    # Bug 🐛 in KeymanWeb: width and pad MUST be strings 🙃
                    # https://github.com/keymanapp/keyman/issues/119
                    key["width"] = str(key["width"])

                    if index > 0:
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
