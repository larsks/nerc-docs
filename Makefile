PYTHON = python3

SRCFILES = $(shell find docs -type f -name '*.in.md')
OUTFILES = $(SRCFILES:.in.md=.md)

%.md: %.in.md
	$(PYTHON) scripts/add_nerc_rates.py -o $@ $<

all: $(OUTFILES)

clean:
	rm -f $(OUTFILES)
