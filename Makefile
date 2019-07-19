TOUCH_LAYOUT = nrc_cr_cans.keyman-touch-layout
KEY_LAYOUT = nrc_cr_cans.kmn

# You gotta chown(1) all of dem first:
DATA = libkeyboard/syllabics.tsv
LIBS = $(wildcard libkeyboard/*.py)

all: $(TOUCH_LAYOUT) $(KEY_LAYOUT)

$(TOUCH_LAYOUT): ./generate-touch-layout.py $(LIBS) $(DATA)
	./$< $@

$(KEY_LAYOUT): ./generate-layout-code.py $(LIBS) $(DATA)
	./$< $@

format:
	black $(wildcard *.py) $(LIBS)

.PHONY: all format
