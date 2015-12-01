include Makefile.settings

SHELL := /bin/bash

DAYS := 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 \
        21 22 23 24 25

PARTS := 1 2

.DELETE_ON_ERROR:

# $(1) = string
define strip_zero
$(patsubst 0%,%,$(1))
endef

# $(1) = day
define input_url
"http://adventofcode.com/day/$(call strip_zero,$(1))/input"
endef

# $(1) = URL
# $(2) = file
define download
wget --no-cookies --header "Cookie: $(COOKIE)" $(1) -q -O- >$(2)
endef

################################################################

# $(1) = day
# $(2) = part
define gen_day_part_template
gen/$(1)/$(2): input/$(1) code/$(1)/$(2).py
	@mkdir -p $$(dir $$@)
	code/$(1)/$(2).py input/$(1) > gen/$(1)/$(2)
endef

$(foreach day,$(DAYS), \
  $(foreach part,$(PARTS), \
    $(eval $(call gen_day_part_template,$(day),$(part)))))

################################################################

# $(1) = day
define input_day_template
input/$(1):
	@mkdir -p $$(dir $$@)
	$(call download,$(call input_url,$(1)),$$@)
endef

$(foreach day,$(DAYS), \
  $(eval $(call input_day_template,$(day))))

################################################################

.PHONY: clean
clean:
	rm -rf gen/ input/
