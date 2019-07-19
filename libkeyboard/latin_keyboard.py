"""
The keyboard layers for

 - latin_lower
 - latin_upper
 - numeric

"""

SYLLABICS_KEY = {"id": "K_SCROLL", "text": "ᓀᐦᐃᔭᐤ", "nextlayer": "default"}

# Note: This was mostly copy-pasted from Keyman's default touch-optimized layout.
LATIN_LAYERS = [
    {
        "id": "latin_lower",
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
                    {"id": "T_new_435", "text": "", "width": "10", "sp": "10"},
                ],
            },
            {
                "id": 3,
                "key": [
                    {
                        "id": "K_SHIFT",
                        "text": "*Shift*",
                        "sp": "1",
                        "nextlayer": "latin_upper",
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
                            {"text": "!", "id": "K_1", "layer": "latin_upper"},
                            {"text": "?", "id": "K_SLASH", "layer": "latin_upper"},
                            {"text": "'", "id": "K_QUOTE"},
                            {"text": '"', "id": "K_QUOTE", "layer": "latin_upper"},
                            {"text": "\\", "id": "K_BKSLASH"},
                            {"text": ":", "id": "K_COLON", "layer": "latin_upper"},
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
        "id": "latin_upper",
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
                    {"id": "K_A", "text": "A", "pad": "50"},
                    {"id": "K_S", "text": "S"},
                    {"id": "K_D", "text": "D"},
                    {"id": "K_F", "text": "F"},
                    {"id": "K_G", "text": "G"},
                    {"id": "K_H", "text": "H"},
                    {"id": "K_J", "text": "J"},
                    {"id": "K_K", "text": "K"},
                    {"id": "K_L", "text": "L"},
                    {"id": "T_new_160", "text": "", "width": "10", "sp": "10"},
                ],
            },
            {
                "id": 3,
                "key": [
                    {
                        "id": "K_SHIFT",
                        "text": "*Shift*",
                        "sp": "2",
                        "nextlayer": "latin_lower",
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
                            {"text": ",", "id": "K_COMMA", "layer": "latin_lower"},
                            {"text": "!", "id": "K_1", "layer": "latin_upper"},
                            {"text": "?", "id": "K_SLASH", "layer": "latin_upper"},
                            {"text": "'", "id": "K_QUOTE", "layer": "latin_lower"},
                            {"text": '"', "id": "K_QUOTE", "layer": "latin_upper"},
                            {"text": "\\", "id": "K_BKSLASH", "layer": "latin_lower"},
                            {"text": ":", "id": "K_COLON", "layer": "latin_upper"},
                            {"text": ";", "id": "K_COLON", "layer": "latin_lower"},
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
                    {"id": "K_4", "text": "$", "pad": "50", "layer": "latin_upper"},
                    {"id": "K_2", "text": "@", "layer": "latin_upper"},
                    {"id": "K_3", "text": "#", "layer": "latin_upper"},
                    {"id": "K_5", "text": "%", "layer": "latin_upper"},
                    {"id": "K_6", "text": "&", "layer": "latin_upper"},
                    {"id": "K_HYPHEN", "text": "_", "layer": "latin_upper"},
                    {"id": "K_EQUAL", "text": "=", "layer": "latin_lower"},
                    {"id": "K_BKSLASH", "text": "|", "layer": "latin_upper"},
                    {"id": "K_BKSLASH", "text": "\\", "layer": "latin_lower"},
                    {"id": "T_new_228", "text": "", "width": "10", "sp": "10"},
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
                        "nextlayer": "latin_lower",
                    },
                    {
                        "id": "K_LBRKT",
                        "text": "[",
                        "pad": "",
                        "sk": [
                            {"id": "U_00AB", "text": "«"},
                            {"id": "K_COMMA", "text": "<", "layer": "latin_upper"},
                            {"id": "K_LBRKT", "text": "{", "layer": "latin_upper"},
                        ],
                    },
                    {"id": "K_9", "text": "(", "layer": "latin_upper"},
                    {"id": "K_0", "text": ")", "layer": "latin_upper"},
                    {
                        "id": "K_RBRKT",
                        "text": "]",
                        "sk": [
                            {"id": "U_00BB", "text": "»"},
                            {"id": "K_PERIOD", "text": ">", "layer": "latin_upper"},
                            {"id": "K_RBRKT", "text": "}", "layer": "latin_upper"},
                        ],
                    },
                    {"id": "K_EQUAL", "text": "+", "layer": "latin_upper"},
                    {"id": "K_HYPHEN", "text": "-"},
                    {"id": "K_8", "text": "*", "layer": "latin_upper"},
                    {"id": "K_SLASH", "text": "/"},
                    {"id": "K_BKSP", "text": "*BkSp*", "width": "100", "sp": "1"},
                ],
            },
            {
                "id": 4,
                "key": [
                    SYLLABICS_KEY,
                    {"id": "K_LOPT", "text": "*Menu*", "width": "120", "sp": "1"},
                    {"id": "K_SPACE", "text": "", "width": "610", "sp": "0"},
                    {"id": "K_ENTER", "text": "*Enter*", "width": "150", "sp": "1"},
                ],
            },
        ],
    },
]
