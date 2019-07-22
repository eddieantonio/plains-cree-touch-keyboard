KEYBOARD_NAME = nrc_crk_cans

TOUCH_LAYOUT = $(OUTDIR)/$(KEYBOARD_NAME).keyman-touch-layout
KEY_LAYOUT = $(OUTDIR)/$(KEYBOARD_NAME).kmn

# Assuming that we're in extras/
# we should place the touch layout and keyboard code in source/
OUTDIR = ../source

# Dependencies.
DATA = libkeyboard/syllabics.tsv
# You gotta chown(1) all of dem first:
LIBS = $(wildcard libkeyboard/*.py)

all: $(TOUCH_LAYOUT) $(KEY_LAYOUT)

$(TOUCH_LAYOUT): ./generate-touch-layout.py $(LIBS) $(DATA)
	./$< $@

$(KEY_LAYOUT): ./generate-kmn.py $(LIBS) $(DATA)
	./$< $@

format:
	black $(wildcard *.py) $(LIBS)

.PHONY: all format
