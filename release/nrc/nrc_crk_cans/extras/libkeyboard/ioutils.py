#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright © 2019 Eddie Antonio Santos <Eddie.Santos@nrc-cnrc.gc.ca>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

# Sentinel value lets you know if filename was not provided as arguments at
# all.
_unspecified = object()


def setup_output(filename: str = _unspecified):
    """
    Sets up output based on command line arguments.

    If there is exactly one argument, that argument is assumed to be a
    filename to write output to.

    If no arguments are passed, then output is directed to stdout.

    stdout is always opened in UTF-8, regardless of system settings. This is
    mostly only an issue in Windows, where the encoding often defaults to some
    weird CP12?? that is incompatible with Candian Aboriginal Syllabics 😡
    """

    if filename is _unspecified and len(sys.argv) == 2:
        filename = sys.argv[1]

    if filename:
        # Assume the first argument is a file to overwrite
        sys.stdout = open(filename, "w", encoding="UTF-8")
    else:
        # To prevent Windows from using CP1252 or something dumb:
        sys.stdout.reconfigure(encoding="UTF-8")
