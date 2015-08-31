# Author: Wu Zhangjin / Falcon <wuzhangjin@gmail.com>
# Update: 2014/01/17 PM 14:20

SRC = $(wildcard *.md)

html_theme=dzslides
latex_theme=Darmstadt
latex_template=./templates/zh_template.tex

PDFS=$(SRC:.md=.pdf)
HTML=$(SRC:.md=.html)

all: clean $(PDFS) $(HTML)

pdf: $(PDFS)

html: $(HTML)

%.pdf: %.md $(latex_template)
	pandoc -t beamer -V theme:$(latex_theme) -V fontsize:9pt $< -o $@ \
	  --toc --template=$(latex_template) --latex-engine=xelatex

%.html: %.md
	pandoc -t $(html_theme) -s --mathjax $< -o $@

read: $(PDFS)
	evince $< &

read-html: $(HTML)
	chromium-browser $<

clean:
	rm -rf *.log *.out *.nav *.aux *.toc *.snm *.bbl *.blg *.tex *.vrb

distclean: clean
	rm -rf *.pdf *.html
