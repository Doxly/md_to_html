# --*-- coding: utf-8 --*--

""" This is wrap around markdown2.py call for generate whole html file 
insteed of body content. 
Markdown file must be in UTF-8 encoding.
Result file would bi in UTF-8 encoding.

Author Pichugin Viacheslav.
2015

Usage: mdtohtml.py <file name>
"""

import markdown2
import os, sys, codec
print "mdtohtml call"