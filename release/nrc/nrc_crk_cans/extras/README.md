
Plains Cree Touch Keyboard generator
====================================

I've written code here that generates a `.keyman-touch-layout` JSON file
and a `.kmn` Keyman programming language file, that, put together,
create a keyboard for writing ᒐᐦᑭᐯᐘᓯᓇᐦᐃᑫᐏᐣ (Plains Cree syllabics).


Requirements
------------

 * Python 3.7+
 * (optional) `make`
 * (optional) [Black](https://github.com/python/black)


Usage
-----

Run `make` to build `nrc_crk_cans.keyman-touch-layout` and `nrc_crk_cans.kmn`.

If you don't have `make`, you can run:

    python3 generate-touch-layout.py ../source/nrc_crk_cans.keyman-touch-layout
    python3 generate-kmn.py ../source/nrc_crk_cans.kmn


Copying
-------

Copyright © 2019 Eddie Antonio Santos of the National Research Council
Canada <Eddie.Santos@nrc-crnc.gc.ca>.

This code is distributed under the terms of the [Mozilla Public License
(MPL) 2.0](https://www.mozilla.org/en-US/MPL/2.0/). See LICENSE for the
full license text.