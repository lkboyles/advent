include Makefile.settings

SHELL := /bin/bash
PYTHON3 := /usr/bin/env python3

DAYS := 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 \
        21 22 23 24 25
PARTS := 1 2

ALL_GEN :=
ALL_INPUT :=
ALL_TEST :=

print-%: ; @echo $*=$($*)

.DELETE_ON_ERROR:

# $(1) = day
# $(2) = part
define code/2
$(call code/1,$(1))/part_$(2).py
endef

# $(1) = day
define code/1
code/$(1)
endef

# $(1) = day
define input/1
input/$(1)
endef

# $(1) = day
# $(2) = part
define gen/2
$(call gen/1,$(1))/$(2)
endef

# $(1) = day
define gen/1
gen/$(1)
endef

# $(1) = day
# $(2) = part
define test/2
$(call test/1,$(1))/$(2)
endef

# $(1) = day
define test/1
test/$(1)
endef

# $(1) = script
define test_python
$(PYTHON3) -m doctest $(1)
endef

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
ifneq ($(wildcard $(call code/2,$(1),$(2))),)
ALL_GEN += $(call gen/2,$(1),$(2))
$(call gen/2,$(1),$(2)): $(call input/1,$(1)) $(call code/2,$(1),$(2))
	@mkdir -p $$(dir $$@)
	$(call code/2,$(1),$(2)) $(call input/1,$(1)) > $(call gen/2,$(1),$(2))
endif
endef

$(foreach day,$(DAYS), \
  $(foreach part,$(PARTS), \
    $(eval $(call gen_day_part_template,$(day),$(part)))))

# $(1) = day
define gen_day_all_template
.PHONY: $(call gen/2,$(1),all)
$(call gen/2,$(1),all): $(filter $(call gen/2,$(1),)%,$(ALL_GEN))
endef

$(foreach day,$(DAYS), \
  $(eval $(call gen_day_all_template,$(day))))

$(call gen/1,all): $(ALL_GEN)

################################################################

# $(1) = day
define input_day_template
ifneq ($(wildcard $(call code/2,$(1),1)),)
ALL_INPUT += $(call input/1,$(1))
$(call input/1,$(1)):
	@mkdir -p $$(dir $$@)
	$(call download,$(call input_url,$(1)),$$@)
endif
endef

$(foreach day,$(DAYS), \
  $(eval $(call input_day_template,$(day))))

$(call input/1,all): $(ALL_INPUT)

################################################################

# $(1) = day
# $(2) = part
define test_day_part_template
ifneq ($(wildcard $(call code/2,$(1),$(2))),)
ALL_TEST += $(call test/2,$(1),$(2))
.PHONY: $(call test/2,$(1),$(2))
$(call test/2,$(1),$(2)):
	$(call test_python,$(call code/2,$(1),$(2)))
endif
endef

$(foreach day,$(DAYS), \
  $(foreach part,$(PARTS), \
    $(eval $(call test_day_part_template,$(day),$(part)))))

# $(1) = day
define test_day_all_template
.PHONY: $(call test/2,$(1),all)
$(call test/2,$(1),all): $(filter $(call test/2,$(1),)%,$(ALL_TEST))
endef

$(foreach day,$(DAYS), \
  $(eval $(call test_day_all_template,$(day))))

$(call test/1,all): $(ALL_TEST)

################################################################

.PHONY: clean
clean:
	rm -rf gen/ input/
