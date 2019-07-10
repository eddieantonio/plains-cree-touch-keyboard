TOUCH_LAYOUT = nrc_cr_cans.keyman-touch-layout
KEY_LAYOUT = nrc_cr_cans.kmn

all: $(TOUCH_LAYOUT) $(KEY_LAYOUT)

$(TOUCH_LAYOUT): ./generate-touch-layout.py syllabics.py syllabics.tsv plains_cree_constants.py
	./$< $@

$(KEY_LAYOUT): ./generate-layout-code.py syllabics.py syllabics.tsv plains_cree_constants.py
	./$< $@

format:
	black $(wildcard *.py)

.PHONY: all format
