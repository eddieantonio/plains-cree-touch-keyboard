TOUCH_LAYOUT = nrc_cr_cans.kmn.json
KEY_LAYOUT = nrc_cr_cans.kmn

all: $(TOUCH_LAYOUT)

$(TOUCH_LAYOUT): ./generate-touch-layout.py syllabics.py syllabics.tsv
	./$< | tee $@ >/dev/null

$(KEY_LAYOUT): ./generate-key-layout.py syllabics.py syllabics.tsv
	./$< | tee $@ >/dev/null

.PHONY: all
