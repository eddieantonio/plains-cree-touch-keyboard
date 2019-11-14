KEYBOARD_NAME = nrc_crk_cans

TOUCH_LAYOUT = $(OUTDIR)/$(KEYBOARD_NAME).keyman-touch-layout
KMN = $(OUTDIR)/$(KEYBOARD_NAME).kmn

KMN_OPTIONS := $(or $(KMN_OPTIONS), --without-css --with-vowel-hack)
LAYOUT_OPTIONS :=  $(or $(LAYOUT_OPTIONS), --without-latin)

# Assuming that we're in extras/
# we should place the touch layout and keyboard code in source/
OUTDIR = ../source

# Dependencies.
DATA = libkeyboard/syllabics.tsv
# You gotta chown(1) all of dem first:
LIBS = $(wildcard libkeyboard/*.py)

all: $(TOUCH_LAYOUT) $(KMN)

$(TOUCH_LAYOUT): ./generate-touch-layout.py $(LIBS) $(DATA)
	./$< $(LAYOUT_OPTIONS) $@

$(KMN): ./generate-kmn.py $(LIBS) $(DATA)
	./$< $(KMN_OPTIONS) $@

format:
	black $(wildcard *.py) $(LIBS)

.PHONY: all format
