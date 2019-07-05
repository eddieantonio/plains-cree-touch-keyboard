all: layout.json

layout.json: keylayout.py syllabics.tsv
	./$< | tee layout.json >/dev/null

.PHONY: all
