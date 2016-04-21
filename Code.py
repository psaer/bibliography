from __future__ import (absolute_import, division, print_function,unicode_literals)
from citeproc.py2compat import *

# The references are parsed from a BibTeX database, so we import the
# corresponding parser.
from citeproc.source.bibtex import BibTeX
import os
import string
# Import the citeproc-py classes we'll use below.
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import formatter
from citeproc import Citation, CitationItem

my_cities=[]
numbering_txt=True

def get_cities(input_file):
    parse_file=open(input_file, 'r', encoding='utf8')
    depth=0
    reading=False
    temp=""   
    for char in parse_file.read():
        if(char=='{'):
            if(depth==0):
                reading=True
            depth=depth+1
        elif (char=='}'):
            depth=depth-1
        elif (char==','):
            if(depth==1 and reading):
                reading=False
                my_cities.append(temp)
                temp=""
        elif reading and char!=' ':
            temp=temp+char
    parse_file.closed
def write_to_txt(filename, bibliography):
    i=1
    f = open(filename,'w', encoding='utf8')
    for item in bibliography.bibliography():
        if(numbering_txt):
            f.write(unicode(str(i))+'. ')
            i=i+1
        f.write(unicode(str(item))+'\n')
    f.close()
def write_to_bbl(filename, bibliography):
    f = open(filename,'w', encoding='utf8')
    f.write('\\begin{thebibliography}{}\n')
    i=0
    for item in bibliography.bibliography():
        f.write('\\bibitem{'+my_cities[i]+'}')
        f.write(unicode(str(item))+'\n')
        i=i+1
    f.write('\\end{thebibliography}')
    f.close()

bib_source = BibTeX('literature.bib', encoding='utf8')
bib_style = CitationStylesStyle('gost-r-7-0-5-2008', locale='ru-RU', validate=False)
bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.plain)

get_cities('literature.bib')
for i in range(len(my_cities)):
    bibliography.register(Citation([CitationItem(my_cities[i])]))

write_to_txt('my_bibliography.txt',bibliography)
write_to_bbl('my_bibliography.bbl',bibliography)