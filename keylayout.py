#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re

layout = """
[ s ] [ w ] [ m ] [ l ] [ r ] [ â ] [ i ] [ î ]
[ hk] [ t ] [ k ] [ h ] [ p ] [ a ] [ o ] [ c ]
[ABC] [ y ] [ n ] [  NNBSP  ] [ ê ] [ ô ] [ BS]
[123] [INT] [         SP          ] [ . ] [ CR]
"""

COMBINING_CONSONANTS = 'ptkcmny'
VOWELS = 'êiîoôaâ'


class Key:
    proportional_width = 1

    def __init__(self, label):
        self.label = label

    @classmethod
    def label_matches(cls, tag):
        return True

    def dictionary_for_mode(self, mode):
        assert mode in ('V', 'CV', 'CwV')
        return dict(id=0, text='ᕽ')

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}({self.label!r})"


class SpaceKey(Key):
    proportional_width = 4

    @classmethod
    def label_matches(cls, tag):
        return tag == 'SP'

    def dictionary_for_mode(self, mode):
        assert mode in ('V', 'CV', 'CwV')
        return dict(id=0, text='ᕽ')

class VowelKey(Key):
    @classmethod
    def label_matches(cls, tag):
        return tag in VOWELS


class NNBSPKey(Key):
    proportional_width = 2

    @classmethod
    def label_matches(cls, tag):
        return tag == 'NNBSP'


class PeriodKey(Key):
    @classmethod
    def label_matches(cls, tag):
        return tag == '.'


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
rows = []
for raw_keys in raw_rows:
    row = []
    for match in re.finditer(r'''\[\s*(\w+)\s*\]''', raw_keys):
        label = match.group(1)
        for cls in (CombiningConsonantKey, VowelKey, PeriodKey, NNBSPKey, SpaceKey, SpecialKey, Key):
            if cls.label_matches(label):
                break
        key = cls(label)
        row.append(key)
    rows.append(row)
