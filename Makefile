# You should only have to modify RELEASED and SOLUTIONS.
# Also change SRC once per semester.

RELEASED = mentor02 mentor05
SOLUTIONS = mentor02

DST = published
SRC = src/sp21

DEPEND = python make_dependency.py
TEX = pdflatex
TEX_FLAGS = -halt-on-error -output-directory ../../$(DST)

SOURCES = $(wildcard $(SRC)/*.tex)
HANDOUT = $(SOURCES:$(SRC)/%.tex=%)
HANDOUT_SOL = $(addsuffix _sol, $(HANDOUT))
HANDOUT_GUIDE = $(addsuffix _guide, $(HANDOUT))

#################################################################
# User-friendly targets: use the following to publish material. #
#################################################################

all: $(RELEASED) $(addsuffix _sol, $(SOLUTIONS)) $(addsuffix _guide, $(SOLUTIONS))

clean:
	find . -name "deps" -type d -prune -exec rm -rf {} \;
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf $(DST)/*

.SECONDEXPANSION:
$(HANDOUT) $(HANDOUT_SOL) $(HANDOUT_GUIDE): $(DST) $(DST)/$$@.pdf

$(DST)/%.pdf: $(SRC)/%.tex commonheader.sty
	$(DEPEND) $* $< deps
	cd $(SRC); $(TEX) $(TEX_FLAGS) $*.tex;
	@-rm $(DST)/*.aux $(DST)/*.log $(DST)/*.out
	#open $(DST)/$*.pdf

$(DST)/%_sol.pdf: $(SRC)/%.tex commonheader.sty
	$(DEPEND) $* $< deps
	cd $(SRC); $(TEX) $(TEX_FLAGS) -jobname="$*_sol" "\def\discussionsolutions{}\input{$*}"
	@-rm $(DST)/*.aux $(DST)/*.log $(DST)/*.out
	#open $(DST)/$*_sol.pdf

$(DST)/%_guide.pdf: $(SRC)/%.tex commonheader.sty
	$(DEPEND) $* $< deps
	cd $(SRC); $(TEX) $(TEX_FLAGS) -jobname="$*_guide" "\def\discussionsolutions{}\def\discussionguides{}\input{$*}"
	@-rm $(DST)/*.aux $(DST)/*.log $(DST)/*.out
	#open $(DST)/$*_guide.pdf

$(DST):
	mkdir -p $@

# Include dependencies that are created by $(DEPEND). These
# dependencies are primarily based on \subimport directives.
-include $(SOURCES:%=deps/%.d)
