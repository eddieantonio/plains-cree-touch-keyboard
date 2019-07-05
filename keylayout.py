#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import csv
import json
import re
import sys
from typing import NamedTuple

LAYOUT = """
[  s  ] [  w   ] [ m ] [ l ] [ r ] [ â ] [ i ] [  î ]
[  hk ] [  t   ] [ k ] [ h ] [ p ] [ a ] [ o ] [  c ]
[ ABC ] [  y   ] [ n ] [  NNBSP  ] [ ê ] [ ô ] [ BS ]
[ 123 ] [ MENU ] [         SP          ] [ . ] [ CR ]
"""

COMBINING_CONSONANTS = "ptkcmnsy"
VOWELS = "êiîoôaâ"

KEY_WIDTH = 150
PADDING_BETWEEN = 3

# Key types
# https://help.keyman.com/developer/10.0/guides/develop/creating-a-touch-keyboard-layout-for-amharic-the-nitty-gritty#id488808
SPECIAL_KEY = "1"  # TODO: for vowels?
ACTIVE_KEY = "2"  # TODO: for active consonant?
SPACER = "10"


class Syllabic(NamedTuple):
    cans: str
    sro: str
    scalar_value: int

    @property
    def key_code(self):
        return f"U_{self.scalar_value:04X}"

    @classmethod
    def from_tsv(cls, row):
        return cls(
            cans=row["cans"], sro=row["latn"], scalar_value=int(row["scalar.value"])
        )


class Key:
    proportional_width = 1

    def __init__(self, label):
        self.label = label

    @classmethod
    def label_matches(cls, tag):
        return True

    def dictionary_for_key(self):
        syllabic = syllabics[self.label]
        return dict(
            id=syllabic.key_code, text=syllabic.cans, width=self.effective_width
        )

    def dictionary_for_key_with_mode(self, mode, consonant):
        assert mode in ("CV", "CwV")
        return self.dictionary_for_key()

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}({self.label!r})"

    @property
    def effective_width(self):
        padding = (self.proportional_width - 1) * PADDING_BETWEEN
        return self.proportional_width * KEY_WIDTH + padding


class VowelKey(Key):
    @classmethod
    def label_matches(cls, tag):
        return tag in VOWELS

    def dictionary_for_key_with_mode(self, mode, consonant):
        sro = mode.replace("C", consonant).replace("V", self.label)
        try:
            syllabic = syllabics[sro]
        except KeyError:
            # nw exceptional cases. Place a spacer here
            assert sro.startswith("nw")
            return dict(
                id="K_ESC",  # Dunno what code to output 🤷
                sp=SPACER,
                width=self.effective_width,
            )
        else:
            return dict(id=syllabic.key_code, text=syllabic.cans, nextlayer="default")


class PeriodKey(Key):
    @classmethod
    def label_matches(cls, tag):
        return tag == "."

    def dictionary_for_key(self):
        return {
            "id": "U_166E",
            "text": "᙮",
            "sk": [{"text": "!", "id": "U_0021"}, {"text": "?", "id": "U_0022"}],
        }


class SpecialKey(Key):
    SETTINGS = {
        "SP": dict(id="K_SPACE", text="", width=4, nextlayer="default", sp="0"),
        "BS": dict(id="K_BKSP", text="*BkSp*", nextlayer="default", sp=SPECIAL_KEY),
        "123": dict(id="K_NUMLOCK", text="*123*", nextlayer="default", sp=SPECIAL_KEY),
        "NNBSP": dict(id="U_202F", text="", width=2, nextlayer="default", sp="0"),
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
        )

    @property
    def proportional_width(self):
        return self.SETTINGS[self.label].get("width", 1)

    @classmethod
    def label_matches(cls, tag):
        return tag in cls.SETTINGS


class CombiningConsonantKey(Key):
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


def parse_syllabics():
    """
    Parse the syllabics TSV file.

    This file should be obtained at:
    https://github.com/UAlbertaALTLab/nehiyawewin-syllabics/blob/master/syllabics.tsv
    """
    syllabics = {}
    with open("./syllabics.tsv") as syllabics_file:
        syllabics_tsv = csv.DictReader(syllabics_file, delimiter="\t")
        for row in syllabics_tsv:
            syllabic = Syllabic.from_tsv(row)
            assert syllabic.sro not in syllabics
            syllabics[syllabic.sro] = syllabic
    return syllabics


def parse_ascii_layout(layout: str) -> list:
    """
    Parses the ASCII art keyboard into a list of rows, each row containing a
    Key.
    """
    raw_rows = layout.strip().split("\n")
    keyboard = []
    for raw_keys in raw_rows:
        row = []
        for match in re.finditer(r"""\[\s*(\w+)\s*\]""", raw_keys):
            label = match.group(1)
            for cls in (CombiningConsonantKey, VowelKey, PeriodKey, SpecialKey, Key):
                if cls.label_matches(label):
                    break
            key = cls(label)
            row.append(key)
        keyboard.append(row)
    return keyboard


#################################### Main ####################################

# Parse the table of syllabics, as well as the keyboard layout.
syllabics = parse_syllabics()
keyboard = parse_ascii_layout(LAYOUT)

# Create the JSON
layers = []
for consonant in ("", *COMBINING_CONSONANTS):
    for mode in ("CV", "CwV"):
        layer_id = (
            "default"
            if consonant == "" and mode == "CV"
            else mode.replace("C", consonant)
        )
        layout_rows = []
        for rowid, row in enumerate(keyboard, start=1):
            layout_rows.append(
                {
                    "id": rowid,
                    "key": [
                        key.dictionary_for_key_with_mode(mode, consonant) for key in row
                    ],
                }
            )
        layers.append(dict(id=layer_id, row=layout_rows))

show_json = True
if show_json:
    json.dump(
        {"phone": {"font": "Euphemia", "layer": layers, "displayUnderlying": False}},
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    print()
else:
    from pprint import pprint

    pprint(syllabics)
