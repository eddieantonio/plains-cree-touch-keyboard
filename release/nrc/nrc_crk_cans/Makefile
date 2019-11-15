# Path to the keymanapp/keyboards repo:
KEYBOARDS_REPO = $(HOME)/Work/keyboards
# Where to copy files
PACKAGE_DESTINATION = $(KEYBOARDS_REPO)/release/nrc/nrc_crk_cans

# Build all of the keyboards and stuff
all:
	$(MAKE) -C extras

include manifest.mk
copy: all $(PACKAGE_FILES)
	find $(PACKAGE_FILES) -print0 | cpio -p -0dv $(PACKAGE_DESTINATION)

.phony: all copy
