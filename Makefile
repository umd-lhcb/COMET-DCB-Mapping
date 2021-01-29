# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Jan 29, 2021 at 02:41 PM +0100

export PATH	:= $(shell pwd):$(PATH)

OUTPUT_PATH	:=	output
VPATH := $(OUTPUT_PATH)

#########
# Rules #
#########

.PHONY: all
all: \
	P2B2toPPP-C-TOP-MAG-TRUE-Alpha.pdf \
	P2B2toPPP-C-TOP-MAG-TRUE-Beta.pdf \
	P2B2toPPP-C-TOP-MAG-TRUE-Gamma.pdf \
	P2B2toPPP-C-BOT-IP-TRUE-Alpha.pdf \
	P2B2toPPP-C-BOT-IP-TRUE-Beta.pdf \
	P2B2toPPP-C-BOT-IP-TRUE-Gamma.pdf

.PHONY: clean
clean:
	@rm -rf $(OUTPUT_PATH)/*

P2B2toPPP-C-TOP-MAG-TRUE-Alpha.csv P2B2toPPP-C-TOP-MAG-TRUE-Beta.csv P2B2toPPP-C-TOP-MAG-TRUE-Gamma.csv \
P2B2toPPP-C-TOP-MAG-TRUE-Alpha.tex P2B2toPPP-C-TOP-MAG-TRUE-Beta.tex P2B2toPPP-C-TOP-MAG-TRUE-Gamma.tex \
P2B2toPPP-C-BOT-IP-TRUE-Alpha.csv P2B2toPPP-C-BOT-IP-TRUE-Beta.csv P2B2toPPP-C-BOT-IP-TRUE-Gamma.csv \
P2B2toPPP-C-BOT-IP-TRUE-Alpha.tex P2B2toPPP-C-BOT-IP-TRUE-Beta.tex P2B2toPPP-C-BOT-IP-TRUE-Gamma.tex \
&: \
	TrueP2B2toPPPMapping.py UT_Aux_mapping/helpers.py UT_Aux_mapping/tabular.py \
	input/true_p2b2.net input/true_ppp_mag.wirelist input/true_ppp_ip.wirelist
	$<

P2B2toPPP-C-BOT-MAG-MIRROR-Alpha.csv P2B2toPPP-C-BOT-MAG-MIRROR-Beta.csv P2B2toPPP-C-BOT-MAG-MIRROR-Gamma.csv \
P2B2toPPP-C-TOP-IP-MIRROR-Alpha.csv P2B2toPPP-C-TOP-IP-MIRROR-Beta.csv P2B2toPPP-C-TOP-IP-MIRROR-Gamma.csv \
P2B2toPPP-C-BOT-MAG-MIRROR-Alpha.tex P2B2toPPP-C-BOT-MAG-MIRROR-Beta.tex P2B2toPPP-C-BOT-MAG-MIRROR-Gamma.tex \
P2B2toPPP-C-TOP-IP-MIRROR-Alpha.tex P2B2toPPP-C-TOP-IP-MIRROR-Beta.tex P2B2toPPP-C-TOP-IP-MIRROR-Gamma.tex &: \
	MirrorP2B2toPPPMapping.py UT_Aux_mapping/helpers.py UT_Aux_mapping/tabular.py \
	input/mirror_p2b2.net input/mirror_ppp.wirelist
	$<


####################
# Generic patterns #
####################

%.pdf: %.tex
	@pdflatex -output-directory $(OUTPUT_PATH) $<
	@pdflatex -output-directory $(OUTPUT_PATH) $<
