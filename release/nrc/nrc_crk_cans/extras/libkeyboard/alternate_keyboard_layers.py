"""
The keyboard layers for

 - numeric
 - latin/shift -- Note: This "shift" is special-cased in KeymanWeb!

"""

SYLLABICS_KEY = {"id": "K_SCROLL", "text": "ᓀᐦᐃᔭᐤ", "nextlayer": "default", "sp": "1"}
WIDE_SYLLABICS_KEY = {**SYLLABICS_KEY, "width": "150"}

NUMERIC_LAYERS = [
    {
        "id": "numeric",
        "row": [
            {
                "id": 1,
                "key": [
                    {"id": "K_1", "text": "1"},
                    {"id": "K_2", "text": "2"},
                    {"id": "K_3", "text": "3"},
                    {"id": "K_4", "text": "4"},
                    {"id": "K_5", "text": "5"},
                    {"id": "K_6", "text": "6"},
                    {"id": "K_7", "text": "7"},
                    {"id": "K_8", "text": "8"},
                    {"id": "K_9", "text": "9"},
                    {"id": "K_0", "text": "0"},
                ],
            },
            {
                "id": 2,
                "key": [
                    # Delaney and I came up with the following keys that SHOULD be easily accessible:
                    #  $ -- for money
                    #  @ -- for email addresses and for @ing people
                    #  # -- for hashtags/social media
                    #  % -- for percentages
                    #  «/» -- for quotations
                    #  / -- for division
                    #  + -- for addition (can be confused with y final)
                    #  - -- for subtraction (can be confused with c final)
                    #  * -- for multiplication
                    #  = -- for equations
                    #
                    # N.B.: Delaney is a mathematician...
                    #
                    # Arden says the comma is essential:
                    #  , -- separating clauses
                    #
                    # Dubious keys:
                    #  " -- use angle quotes instead (can be confused for h)
                    #  \ -- Only useful for coding?
                    #  ` -- Only useful for coding?
                    #  ~ -- Only useful for coding?
                    #  | -- Only useful for coding?
                    #  ^ -- Only useful for coding?
                    #  ; -- Not used in syllabics -- too many dots
                    #  : -- Not used in syllabics -- too many dots
                    #  ' -- Not used in syllabics (can be confused for p final)
                    #
                    # On the fence:
                    #  _ -- user names???
                    #  & -- just write êkwa instead?
                    {"id": "K_2", "text": "@", "layer": "shift"},
                    {"id": "K_3", "text": "#", "layer": "shift"},
                    {"id": "K_4", "text": "$", "layer": "shift"},
                    # TODO: remove this?
                    {"id": "K_7", "text": "&", "layer": "shift"},
                    {"id": "K_HYPHEN", "text": "_", "layer": "shift"},
                    {"id": "K_HYPHEN", "text": "-"},
                    {
                        "id": "K_9",
                        "text": "(",
                        "layer": "shift",
                        "sk": [
                            {"id": "K_LBRKT", "text": "["},
                            {"id": "K_COMMA", "text": "<", "layer": "shift"},
                            {"id": "K_LBRKT", "text": "{", "layer": "shift"},
                        ],
                    },
                    {
                        "id": "K_0",
                        "text": ")",
                        "layer": "shift",
                        "sk": [
                            {"id": "K_RBRKT", "text": "]"},
                            {"id": "K_PERIOD", "text": ">", "layer": "shift"},
                            {"id": "K_RBRKT", "text": "}", "layer": "shift"},
                        ],
                    },
                    {"id": "K_EQUAL", "text": "=", "layer": "latin"},
                    {"id": "K_5", "text": "%", "layer": "shift"},
                ],
            },
            {
                "id": 3,
                "key": [
                    {
                        "id": "K_LOWER",
                        "text": "*abc*",
                        "width": "",
                        "sp": "1",
                        "nextlayer": "latin",
                    },
                    {"id": "U_00AB", "text": "«"},
                    {"id": "K_8", "text": "*", "layer": "shift"},
                    {"id": "U_00BB", "text": "»"},
                    {"id": "K_COMMA", "text": ","},
                    {"id": "K_SLASH", "text": "/"},
                    {"id": "K_1", "text": "!", "layer": "shift"},
                    {"id": "K_SLASH", "text": "?", "layer": "shift"},
                    {"id": "K_EQUAL", "text": "+", "layer": "shift"},
                    {"id": "K_BKSP", "text": "*BkSp*", "width": "100", "sp": "1"},
                ],
            },
            {
                "id": 4,
                "key": [
                    WIDE_SYLLABICS_KEY,
                    {"id": "K_LOPT", "text": "*Menu*", "width": "120", "sp": "1"},
                    {"id": "K_SPACE", "text": "", "width": "610", "sp": "0"},
                    {"id": "K_ENTER", "text": "*Enter*", "width": "150", "sp": "1"},
                ],
            },
        ],
    }
]

# Note: This was mostly copy-pasted from Keyman's default touch-optimized layout.
LATIN_LAYERS = [
    {
        "id": "latin",
        "row": [
            {
                "id": 1,
                "key": [
                    {"id": "K_Q", "text": "q"},
                    {"id": "K_W", "text": "w"},
                    {"id": "K_E", "text": "e"},
                    {"id": "K_R", "text": "r"},
                    {"id": "K_T", "text": "t"},
                    {"id": "K_Y", "text": "y"},
                    {"id": "K_U", "text": "u"},
                    {"id": "K_I", "text": "i"},
                    {"id": "K_O", "text": "o"},
                    {"id": "K_P", "text": "p"},
                ],
            },
            {
                "id": 2,
                "key": [
                    SYLLABICS_KEY,
                    {"id": "K_A", "text": "a"},
                    {"id": "K_S", "text": "s"},
                    {"id": "K_D", "text": "d"},
                    {"id": "K_F", "text": "f"},
                    {"id": "K_G", "text": "g"},
                    {"id": "K_H", "text": "h"},
                    {"id": "K_J", "text": "j"},
                    {"id": "K_K", "text": "k"},
                    {"id": "K_L", "text": "l"},
                ],
            },
            {
                "id": 3,
                "key": [
                    {
                        "id": "K_SHIFT",
                        "text": "*Shifted*",
                        "sp": "1",
                        "nextlayer": "shift",
                    },
                    {"id": "K_Z", "text": "z"},
                    {"id": "K_X", "text": "x"},
                    {"id": "K_C", "text": "c"},
                    {"id": "K_V", "text": "v"},
                    {"id": "K_B", "text": "b"},
                    {"id": "K_N", "text": "n"},
                    {"id": "K_M", "text": "m"},
                    {
                        "id": "K_PERIOD",
                        "text": ".",
                        "sk": [
                            {"text": ",", "id": "K_COMMA"},
                            {"text": "!", "id": "K_1", "layer": "shift"},
                            {"text": "?", "id": "K_SLASH", "layer": "shift"},
                            {"text": "'", "id": "K_QUOTE"},
                            {"text": '"', "id": "K_QUOTE", "layer": "shift"},
                            {"text": "\\", "id": "K_BKSLASH"},
                            {"text": ":", "id": "K_COLON", "layer": "shift"},
                            {"text": ";", "id": "K_COLON"},
                        ],
                    },
                    {"id": "K_BKSP", "text": "*BkSp*", "width": "100", "sp": "1"},
                ],
            },
            {
                "id": 4,
                "key": [
                    {
                        "id": "K_NUMLOCK",
                        "text": "*123*",
                        "width": "150",
                        "sp": "1",
                        "nextlayer": "numeric",
                    },
                    {"id": "K_LOPT", "text": "*Menu*", "width": "120", "sp": "1"},
                    {"id": "K_SPACE", "text": "", "width": "610", "sp": "0"},
                    {"id": "K_ENTER", "text": "*Enter*", "width": "150", "sp": "1"},
                ],
            },
        ],
    },
    {
        "id": "shift",
        "row": [
            {
                "id": 1,
                "key": [
                    {"id": "K_Q", "text": "Q"},
                    {"id": "K_W", "text": "W"},
                    {"id": "K_E", "text": "E"},
                    {"id": "K_R", "text": "R"},
                    {"id": "K_T", "text": "T"},
                    {"id": "K_Y", "text": "Y"},
                    {"id": "K_U", "text": "U"},
                    {"id": "K_I", "text": "I"},
                    {"id": "K_O", "text": "O"},
                    {"id": "K_P", "text": "P"},
                ],
            },
            {
                "id": 2,
                "key": [
                    SYLLABICS_KEY,
                    {"id": "K_A", "text": "A"},
                    {"id": "K_S", "text": "S"},
                    {"id": "K_D", "text": "D"},
                    {"id": "K_F", "text": "F"},
                    {"id": "K_G", "text": "G"},
                    {"id": "K_H", "text": "H"},
                    {"id": "K_J", "text": "J"},
                    {"id": "K_K", "text": "K"},
                    {"id": "K_L", "text": "L"},
                ],
            },
            {
                "id": 3,
                "key": [
                    {
                        "id": "K_SHIFT",
                        "text": "*Shift*",
                        "sp": "2",
                        "nextlayer": "latin",
                    },
                    {"id": "K_Z", "text": "Z"},
                    {"id": "K_X", "text": "X"},
                    {"id": "K_C", "text": "C"},
                    {"id": "K_V", "text": "V"},
                    {"id": "K_B", "text": "B"},
                    {"id": "K_N", "text": "N"},
                    {"id": "K_M", "text": "M"},
                    {
                        "id": "K_PERIOD",
                        "text": ".",
                        "sk": [
                            {"text": ",", "id": "K_COMMA", "layer": "latin"},
                            {"text": "!", "id": "K_1", "layer": "shift"},
                            {"text": "?", "id": "K_SLASH", "layer": "shift"},
                            {"text": "'", "id": "K_QUOTE", "layer": "latin"},
                            {"text": '"', "id": "K_QUOTE", "layer": "shift"},
                            {"text": "\\", "id": "K_BKSLASH", "layer": "latin"},
                            {"text": ":", "id": "K_COLON", "layer": "shift"},
                            {"text": ";", "id": "K_COLON", "layer": "latin"},
                        ],
                    },
                    {"id": "K_BKSP", "text": "*BkSp*", "sp": "1"},
                ],
            },
            {
                "id": 4,
                "key": [
                    {
                        "id": "K_NUMLOCK",
                        "text": "*123*",
                        "width": "150",
                        "sp": "1",
                        "nextlayer": "numeric",
                    },
                    {"id": "K_LOPT", "text": "*Menu*", "width": "120", "sp": "1"},
                    {"id": "K_SPACE", "text": "", "width": "610", "sp": "0"},
                    {"id": "K_ENTER", "text": "*Enter*", "width": "150", "sp": "1"},
                ],
            },
        ],
    },
]
