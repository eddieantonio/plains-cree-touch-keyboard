#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
A mapping between SRO syllables and syllabics.
"""

import csv
from types import MappingProxyType
from typing import NamedTuple

__all__ = ["SYLLABICS"]


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
    with open("./syllabics.tsv") as syllabics_file:
        syllabics_tsv = csv.DictReader(syllabics_file, delimiter="\t")
        for row in syllabics_tsv:
            syllabic = Syllabic.from_tsv(row)
            assert syllabic.sro not in syllabics
            syllabics[syllabic.sro] = syllabic
    return syllabics


# Create a global lookup table that converts an SRO sequence to a syllabic.
# Note: using MappingProxyType makes this table **read-only**.
SYLLABICS = MappingProxyType(_parse_syllabics())
