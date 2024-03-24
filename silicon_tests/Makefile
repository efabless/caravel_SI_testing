TESTS ?= $(wildcard caravel/*)
LOGS = $(addsuffix /make.log,$(TESTS))
all: make_all.log

make_all.log: $(LOGS)
	cat $(LOGS) > $@

.PHONY: $(LOGS)

$(LOGS): %/make.log: %
	make -i -C $< clean
	echo "=== $< ===" | tee $@
	make -i -C $< | tee -a $@
