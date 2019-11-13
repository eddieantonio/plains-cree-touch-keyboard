#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright © 2019 Eddie Antonio Santos <Eddie.Santos@nrc-cnrc.gc.ca>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
A mapping between SRO syllables and syllabics.
"""

import csv
from types import MappingProxyType
from typing import NamedTuple
from pathlib import Path


__all__ = ["SYLLABICS"]
here = Path(__file__).parent

VOWELS = 'êioaîôâ'

class Syllabic(NamedTuple):
    """
    A single syllabic.
    """

    cans: str
    sro: str
    scalar_value: int

    def __str__(self) -> str:
        return self.cans

    @property
    def key_code(self):
        return f"U_{self.scalar_value:04X}"

    @property
    def as_keycode(self):
        return self.key_code

    @property
    def as_character(self):
        return f"U+{self.scalar_value:04X}"

    @property
    def type(self):
        if len(self.sro) == 1:
            if self.sro in VOWELS:
                return 'vowel'
            else:
                return  'consonant'
        else:
            return 'syllable'

    @property
    def prefix(self):
        naive_prefix = self.sro.rstrip(VOWELS)
        if naive_prefix == self.sro:
            return ''
        return naive_prefix

    @property
    def vowel(self):
        if self.type == 'syllable':
            return self.sro[-1]
        elif self.type == 'vowel':
            return self.sro
        raise ValueError(f"no vowel in {self}")

    @classmethod
    def from_tsv(cls, row):
        return cls(
            cans=row["cans"], sro=row["latn"], scalar_value=int(row["scalar.value"])
        )


def _parse_syllabics():
    """
    Parse the syllabics TSV file.

    This file should be obtained at:
    https://github.com/UAlbertaALTLab/nehiyawewin-syllabics/blob/master/syllabics.tsv
    """
    syllabics = {}
    with open(here / "syllabics.tsv", encoding="UTF-8") as syllabics_file:
        syllabics_tsv = csv.DictReader(syllabics_file, delimiter="\t")
        for row in syllabics_tsv:
            syllabic = Syllabic.from_tsv(row)
            assert syllabic.sro not in syllabics
            syllabics[syllabic.sro] = syllabic
    return syllabics


# Create a global lookup table that converts an SRO sequence to a syllabic.
# Note: using MappingProxyType makes this table **read-only**.
SYLLABICS = MappingProxyType(_parse_syllabics())
