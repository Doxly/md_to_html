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

def convert(mdfilename):

    import markdown2
    # print 'mdtohtml call'

    mdencoding = 'utf-8'
    htmlencoding = 'utf-8'

    output = headtemplate

    # Process css
    css = ''
    if "--css" in sys.argv:
        css = '<link rel="stylesheet" href="main.css">'
    output = output.replace('<<css>>',css)

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
    for arg in sys.argv:
        if re.match('.*\.md$|.*\.mdown$|.*\.markdown',arg, re.IGNORECASE):
            mdfilename = arg
            # print 'mdfilename=', mdfilename

    if not 'mdfilename' in locals():
        print "You forgot to enter markdown file name"
        sys.exit(1)

    convert(mdfilename)


if __name__ == '__main__':
    main()