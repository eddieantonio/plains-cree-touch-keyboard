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

from libkeyboard.ioutils import setup_output
from libkeyboard.alternate_keyboard_layers import LATIN_LAYERS, NUMERIC_LAYERS
from libkeyboard.plains_cree_constants import COMBINING_CONSONANTS, VOWELS
from libkeyboard.syllabics import SYLLABICS


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
[  l  ] [  p   ] [ k ] [ s ] [ â ] [ a ] [ o ] [  r ]
[ ABC ] [  c   ] [ t ] [  NNBSP  ] [ ê ] [ h ] [ BS ]
[ 123 ] [ MENU ] [         SP          ] [ . ] [ CR ]
"""

# Keyman defines each key's width as being 100 units.
# The default padding is 5 units.
SLOT_WIDTH = 115  # How much width each "slot" occupies
PADDING_BETWEEN = 15  # How much of the slot is just the padding.
KEY_WIDTH = SLOT_WIDTH - PADDING_BETWEEN  # How much of the slot is the key itself

# Key types
# https://help.keyman.com/developer/10.0/guides/develop/creating-a-touch-keyboard-layout-for-amharic-the-nitty-gritty#id488808
NORMAL_KEY = "0"
SPECIAL_KEY = "1"  # for ABC, 123, Enter, BS, etc.
ACTIVE_KEY = "2"  # for non-default vowel syllabics
DEAD_KEY = "8"  # for active consonant/w.
BLANK_KEY = "9"  # placeholder for missing nwV syllabics
SPACER = "10"  # an empty space, the size of a key

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
        return dict(id=syllabic.key_code, text=syllabic.cans, **self.extra_attributes)

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
                id="", sp=BLANK_KEY, text=""  # A blank code is valid, apparently?
            )
        else:
            result = dict(id=syllabic.key_code, text=syllabic.cans, nextlayer="default")
            # Highlight the vowels that have changed.
            if consonant or sro.startswith("w"):
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
                {"text": ".", "id": "U_002E"},
                {"text": '"', "id": "U_0022"},
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
        # BS should not ALWAYS return to default layer:
        # See: https://github.com/keymanapp/keyman/issues/2349#issuecomment-558459256
        "BS": dict(id="K_BKSP", text="*BkSp*", sp=SPECIAL_KEY),
        "123": dict(id="K_NUMLOCK", text="*123*", nextlayer="numeric", sp=SPECIAL_KEY),
        "NNBSP": dict(
            id="U_202F", text="", width=2, nextlayer="default", sp=SPECIAL_KEY
        ),
        "ABC": dict(id="K_UPPER", text="*ABC*", nextlayer="latin", sp=SPECIAL_KEY),
        "CR": dict(id="K_ENTER", text="*Enter*", nextlayer="default", sp=SPECIAL_KEY),
        "MENU": dict(id="K_LOPT", text="*Menu*", sp=SPECIAL_KEY),
    }

    def dictionary_for_key(self):
        settings = self.SETTINGS[self.label]
        key = dict(id=settings["id"], text=settings["text"], sp=settings["sp"])
        if "nextlayer" in settings:
            key.update(nextlayer=settings["nextlayer"])
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


class BackspaceKey(Key):
    """
    The backspace key changes its nextlayer based on the current layer.
    """

    @classmethod
    def label_matches(cls, tag):
        return tag == "BS"

    def dictionary_for_key_with_mode(self, mode, consonant):
        key = dict(id="K_BKSP", text="*BkSp*", sp=SPECIAL_KEY)

        # The nextlayer depend on the current layer.
        if mode == "CV" and not consonant:
            # Default layer: there should be no layer switching
            nextlayer = None
        elif mode == "CV" or (mode == "CwV" and not consonant):
            # Deleting the final means we go back to the default.
            nextlayer = "default"
        elif mode == "CwV" and not consonant:
            # wV layer: should go back to default!
            nextlayer = "default"
        elif mode == "CwV":
            # Delete the 'w' means we will be typing a CV syllabic
            nextlayer = f"{consonant}V"
        else:
            raise ValueError(f"Don't know how to handle {mode} {consonant}")

        if nextlayer is not None:
            key.update(nextlayer=nextlayer)

        return key

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
                BackspaceKey,
                SpecialKey,
                Key,
            ):
                if cls.label_matches(label):
                    break
            key = cls(label)
            row.append(key)
        keyboard.append(row)
    return keyboard


def create_keyman_touch_layout_json(
    keyboard: list, include_latin: bool = False
) -> dict:
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
                layout_rows.append({"id": rowid, "key": keys})

            layers.append(dict(id=layer_id, row=layout_rows))

    # Add the "numeric" layer(s) to the keyboard:
    layers.extend(NUMERIC_LAYERS)

    # Add "latin", "shift", and "numeric" layers to the keyboard.
    if include_latin:
        layers.extend(LATIN_LAYERS)

    # Post-process the keyboard.
    for layer in layers:
        for row in layer["row"]:
            post_process_keys(row["key"], include_latin)

    phone_layout = {
        "font": "Noto Sans, Gadugi, Euphemia, Euphemia UCAS, Tahoma, sans-serif",
        "layer": layers,
        # I'm not super sure what this flag is even supposed to do, but here's
        # the code that implements it ¯\_(ツ)_/¯
        # https://github.com/keymanapp/keyman/blob/eeb797bf124718559479622dff6031cfe78477f3/windows/src/developer/TIKE/xml/layoutbuilder/builder.js
        "displayUnderlying": False,
    }
    return {"phone": phone_layout}


def post_process_keys(keys, include_latin: bool):
    """
    Do some post-processing on the keys like:

     - converting all width and padding values to string (to account for a KMW
       bug)
     - removing the Latin keyboard, when applicable.
    """
    # Implement workarounds to make the layout render correctly
    for _index, key in enumerate(keys):
        # Bug 🐛 in KeymanWeb: width and pad MUST be strings 🙃
        # https://github.com/keymanapp/keyman/issues/119
        if "width" in key:
            key["width"] = str(key["width"])
        if "pad" in key:
            key["pad"] = str(PADDING_BETWEEN)

        # Replace the *ABC* key with a space when the Latin
        # layers are not included.
        if not include_latin and is_latin_mode_switch_key(key):
            key.update(text="", sp=SPACER)
            del key["nextlayer"]


def is_latin_mode_switch_key(key):
    """
    Returns True when the given key is intended to switch into a Latin layer.
    """
    return key["text"] in ("*ABC*", "*abc*")


#################################### Main ####################################
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("outfile", nargs="?")
    parser.add_argument(
        "--with-latin", action="store_true", dest="latin", default=False
    )
    parser.add_argument("--without-latin", action="store_false", dest="latin")
    args = parser.parse_args()
    setup_output(args.outfile)

    # Parse the table of syllabics, as well as the keyboard layout.
    keyboard = parse_ascii_layout(LAYOUT)

    layout = create_keyman_touch_layout_json(keyboard, include_latin=args.latin)
    json.dump(layout, sys.stdout, indent=2, ensure_ascii=False)
    print()
