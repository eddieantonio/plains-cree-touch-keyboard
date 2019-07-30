#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright © 2019 Eddie Antonio Santos <Eddie.Santos@nrc-cnrc.gc.ca>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys


def setup_output(parser=None):
    """
    Sets up output based on command line arguments.

    If there is exactly one argument, that argument is assumed to be a
    filename to write output to.

    If no arguments are passed, then output is directed to stdout.

    This can also take an argument parser instance, and it will add an
    optional "outfile" positional argument.

    stdout is always opened in UTF-8, regardless of system settings. This is
    mostly only an issue in Windows, where the encoding often defaults to some
    weird CP12?? that is incompatible with Candian Aboriginal Syllabics 😡
    """

    if parser is not None:
        parser.add_argument('outfile', nargs='?')
        args = parser.parse_args()
        if args.outfile:
            sys.stdout = open(args.outfile, "w", encoding="UTF-8")
        else:
          _setup_stdout_utf8()
        return args
    elif len(sys.argv) == 2:
        # Assume the first argument is a file to overwrite
        sys.stdout = open(sys.argv[1], "w", encoding="UTF-8")
    else:
      _setup_stdout_utf8()

def _setup_stdout_utf8():
    # To prevent Windows from using CP1252 or something dumb:
    sys.stdout.reconfigure(encoding="UTF-8")
