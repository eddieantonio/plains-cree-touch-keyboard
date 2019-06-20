#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import csv
import json
import re
import sys
from typing import NamedTuple

layout = """
[ s ] [ w ] [ m ] [ l ] [ r ] [ â ] [ i ] [ î ]
[ hk] [ t ] [ k ] [ h ] [ p ] [ a ] [ o ] [ c ]
[ABC] [ y ] [ n ] [  NNBSP  ] [ ê ] [ ô ] [ BS]
[123] [INT] [         SP          ] [ . ] [ CR]
"""

COMBINING_CONSONANTS = 'ptkcmny'
VOWELS = 'êiîoôaâ'

KEY_WIDTH = 150
PADDING_BETWEEN = 3


class Syllabic(NamedTuple):
    cans: str
    sro: str
    scalar_value: int

    @property
    def key_code(self):
        return f"U_{self.scalar_value:04X}"

    @classmethod
    def from_tsv(cls, row):
        return cls(cans=row['cans'],
                   sro=row['latn'],
                   scalar_value=int(row['scalar.value']))


syllabics = {}

with open('./syllabics.tsv') as syllabics_file:
    syllabics_tsv = csv.DictReader(syllabics_file, delimiter="\t")
    for row in syllabics_tsv:
        syllabic = Syllabic.from_tsv(row)
        assert syllabic.sro not in syllabics
        syllabics[syllabic.sro] = syllabic


class Key:
    proportional_width = 1

    def __init__(self, label):
        self.label = label

    @classmethod
    def label_matches(cls, tag):
        return True

    def dictionary_for_mode(self, mode):
        assert mode in ('V', 'CV', 'CwV')
        syllabic = syllabics[self.label]
        return dict(id=syllabic.key_code,
                    text=syllabic.cans)

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}({self.label!r})"

    @property
    def effective_width(self):
        padding = (self.proportional_width - 1) * PADDING_BETWEEN
        return self.proportional_width * KEY_WIDTH + padding


class SpaceKey(Key):
    proportional_width = 4

    @classmethod
    def label_matches(cls, tag):
        return tag == 'SP'

    def dictionary_for_mode(self, mode):
        assert mode in ('V', 'CV', 'CwV')
        return dict(id="K_SPACE", text="", width=self.effective_width)


class VowelKey(Key):
    @classmethod
    def label_matches(cls, tag):
        return tag in VOWELS


class NNBSPKey(Key):
    proportional_width = 2

    @classmethod
    def label_matches(cls, tag):
        return tag == 'NNBSP'

    def dictionary_for_mode(self, mode):
        return dict(id="U_202F", text="", width=self.effective_width)


class PeriodKey(Key):
    @classmethod
    def label_matches(cls, tag):
        return tag == '.'

    def dictionary_for_mode(self, mode):
        return {
            "id": "U_166E",
            "text": "᙮",
            "sk": [
                {
                    "text": "!",
                    "id": "U_0021"
                },
                {
                    "text": "?",
                    "id": "U_0022"
                }
            ]
        }


class SpecialKey(Key):
    @classmethod
    def label_matches(cls, tag):
        return tag == tag.upper()


class CombiningConsonantKey(Key):
    @classmethod
    def label_matches(cls, tag):
        return tag in COMBINING_CONSONANTS

    def dictionary_for_mode(self, mode):
        assert mode in ('V', 'CV', 'CwV')
        return dict(id=0, text='ᕽ')


# parse keyboard into a series of abstract rows.
raw_rows = layout.strip().split("\n")
keyboard = []
for raw_keys in raw_rows:
    row = []
    for match in re.finditer(r'''\[\s*(\w+)\s*\]''', raw_keys):
        label = match.group(1)
        for cls in (CombiningConsonantKey, VowelKey, PeriodKey, NNBSPKey, SpaceKey, SpecialKey, Key):
            if cls.label_matches(label):
                break
        key = cls(label)
        row.append(key)
    keyboard.append(row)

# Create the JSON
layers = []
for mode in 'V':
    layout_rows = []
    for rowid, row in enumerate(keyboard, start=1):
        layout_rows.append({
            "id": rowid,
            "key": [key.dictionary_for_mode(mode) for key in row]
        })
    layers.append(dict(id="default", row=layout_rows))

show_json = False
if show_json:
    json.dump({
        "phone": {
            "font": "Euphemia",
            "layer": layers,
            "displayUnderlying": False
        }
    }, sys.stdout, indent=2, ensure_ascii=False)
else:
    from pprint import pprint
    pprint(syllabics)
