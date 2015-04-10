#!/usr/bin/env python
# --*-- coding: utf-8 --*--

""" This is wrap around markdown2.py call for generate whole html file 
insteed of body content. 
Markdown file must be in UTF-8 encoding.
Result file would bi in UTF-8 encoding.

Author Pichugin Viacheslav.
2015

Usage: mdtohtml.py <file name>
"""

import os, sys, codecs, re
import argparse

debug = False
headtemplate = """<!DOCTYPE html>
<html lan="eng">
<head>
    <meta type="text/html" charset="utf-8">
    <<css>>
</head>
<body>
"""

tailtemplate = """</body>
</html>
"""

def convert(mdfilename, css):

    import markdown2
    # print 'mdtohtml call'

    mdencoding = 'utf-8'
    htmlencoding = 'utf-8'

    output = headtemplate

    # Process css
    css_str = ''
    if css:
        css_str = '<link rel="stylesheet" href="main.css">'
    output = output.replace('<<css>>',css_str)

    # Process markdown file
    mdfile = codecs.open(mdfilename, 'r', mdencoding)
    text = markdown2.markdown(mdfile.read())
    output += text

    output += tailtemplate

    # Write result
    htmlfilename = mdfilename.split('.')[0]+'.html'
    htmlfile = codecs.open(htmlfilename, 'w', htmlencoding)
    htmlfile.write(output)

    if debug:
        print output

    print "'%s' file created" % (htmlfilename)

def main():
    parser = argparse.ArgumentParser(description = 'Convert given markdown file into HTML-file. Name of HTML-file corresponds to the markdown one.')
    parser.add_argument('-css', '--css', action = 'store_true', dest = 'css', help = 'Enter if you want to link your html file with main.css')
    parser.add_argument('mdfilename', help = 'Markdown file name')
    args = parser.parse_args()

    if not re.match('.*\.md$|.*\.mdown$|.*\.markdown',args.mdfilename, re.IGNORECASE):
        print "You forgot to enter markdown file name"
        sys.exit(1)

    convert(args.mdfilename, args.css)


if __name__ == '__main__':
    main()