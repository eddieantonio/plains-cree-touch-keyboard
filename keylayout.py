#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import csv
import json
import re
import sys
from typing import NamedTuple

layout = """
[  s  ] [   w  ] [ m ] [ l ] [ r ] [ â ] [ i ] [  î ]
[  hk ] [   t  ] [ k ] [ h ] [ p ] [ a ] [ o ] [  c ]
[ ABC ] [   y  ] [ n ] [  NNBSP  ] [ ê ] [ ô ] [ BS ]
[ 123 ] [ MENU ] [         SP          ] [ . ] [ CR ]
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



class VowelKey(Key):
    @classmethod
    def label_matches(cls, tag):
        return tag in VOWELS



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
    SETTINGS = {
        "SP": dict(id='K_SPACE', text="", width=4),
        "BS": dict(id="K_BKSP",  text="*BkSp*"),
        "123": dict(id="K_NUMLOCK", text="*123*"),
        "NNBSP": dict(id="U_202F", text="", width=2),
        "ABC": dict(id="K_UPPER", text="*ABC*"),  # TODO: make alpha layout
        "CR": dict(id="K_ENTER", text="*Enter*"),
        "MENU": dict(id="K_LOPT", text="*Menu*"),
    }

    def dictionary_for_mode(self, mode):
        assert mode in ('V', 'CV', 'CwV')
        settings = self.SETTINGS[self.label]
        return dict(id=settings['id'],
                    text=settings['text'],
                    width=self.effective_width)

    @property
    def proportional_width(self):
        return self.SETTINGS[self.label].get('width', 1)

    @classmethod
    def label_matches(cls, tag):
        return tag in cls.SETTINGS


class CombiningConsonantKey(Key):
    @classmethod
    def label_matches(cls, tag):
        return tag in COMBINING_CONSONANTS


# parse keyboard into a series of abstract rows.
raw_rows = layout.strip().split("\n")
keyboard = []
for raw_keys in raw_rows:
    row = []
    for match in re.finditer(r'''\[\s*(\w+)\s*\]''', raw_keys):
        label = match.group(1)
        for cls in (CombiningConsonantKey, VowelKey, PeriodKey, SpecialKey, Key):
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

show_json = True
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
