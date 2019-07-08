#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Generates the .kmn keyboard code for to make the touch layout work properly.
"""


PREAMBLE = """
store(&VERSION) '10.0'
store(&TARGETS) 'iphone androidphone mobile'
store(&NAME) 'Plains Cree Syllabics Keyboard'
store(&COPYRIGHT) 'Copyright © 2019 National Research Council Canada'
store(&EthnologueCode) 'crk'
store(&KEYBOARDVERSION) '0.1.0'
store(&LAYOUTFILE) 'nrc_cr_cans.keyman-touch-layout'

c TODO: Embed custom CSS?

begin Unicode > use(main)
group(main) using keys
""".lstrip()


print(PREAMBLE)
