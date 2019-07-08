TOUCH_LAYOUT = nrc_cr_cans.kmn.json

all: $(TOUCH_LAYOUT)

$(TOUCH_LAYOUT): keylayout.py syllabics.py syllabics.tsv
	./$< | tee $@ >/dev/null

.PHONY: all
