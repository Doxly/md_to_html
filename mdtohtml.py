#!/usr/bin/env python
# --*-- coding: utf-8 --*--

""" This is wrap around markdown2.py call for generate whole html file 
insteed of body content. 
Markdown file must be in UTF-8 encoding.
Result file would bi in UTF-8 encoding.

Author: Pichugin Viacheslav.
2015
"""

import os
import sys
import codecs
import re
import argparse

_DEBUG = False
MD_ENCODING = 'utf-8'
HTML_ENCODING = 'utf-8'
BOM = u'\ufeff'

head_template = """<!DOCTYPE html>
<html lan="eng">
<head>
    <meta type="text/html" charset="utf-8">
    <<css>>
</head>
<body>
"""

tail_template = """</body>
</html>
"""

def convert(md_file_name, css, encoding):

    import markdown2
    # print 'mdtohtml call'

    output = head_template

    # Process css
    css_str = ''
    if css:
        css_str = '<link rel="stylesheet" href="main.css">'
    output = output.replace('<<css>>',css_str)

    # Process markdown file
    md_file = codecs.open(md_file_name, 'r', encoding)
    md_text = md_file.read();
    # check for BOM 
    # if md_text[0] == BOM:
    if md_text.startswith(BOM):
        md_text = md_text[1:]
        print 'remove BOM'
    text = markdown2.markdown(md_text, extras=['tables', 'wiki-tables'])
    output += text

    output += tail_template

    # Write result
    html_filename = md_file_name.split('.')[0]+'.html'
    html_file = codecs.open(html_filename, 'w', HTML_ENCODING)
    html_file.write(output)

    if _DEBUG:
        print output

    print "'%s' file created" % (html_filename)

def main():
    parser = argparse.ArgumentParser(description = 'Convert given markdown file into HTML-file. Name of HTML-file corresponds to the markdown one.')
    parser.add_argument('-css', '--css', action = 'store_true', dest = 'css', help = 'Enter if you want to link your html file with main.css')
    parser.add_argument('--encoding', default = MD_ENCODING, help = 'Encoding of markdown file. UTF-8 if ommit. You can use cp1251, cp866 etc.')
    parser.add_argument('md_file_name', help = 'Markdown file name')
    args = parser.parse_args()

    if not re.match('.*\.md$|.*\.mdown$|.*\.markdown',args.md_file_name, re.IGNORECASE):
        print "You forgot to enter markdown file name"
        sys.exit(1)

    convert(args.md_file_name, args.css, args.encoding)


if __name__ == '__main__':
    main()