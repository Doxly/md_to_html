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
    <meta type="text/html" charset="%s">
    <<css>>
</head>
<body>
""" % (HTML_ENCODING)

tail_template = """</body>
</html>
"""

class Convertor(object):
    """Main class for the module.
    can be used either from command lile call, or throu API.
    """
    def __init__(self):
        super(Convertor, self).__init__()


    def convert(self, md_file_name, css, encoding):
        """
        Process markdown file with given name.
        Write result into the file with the same name and extension ".html".
        """

        # Process markdown file
        md_file = codecs.open(md_file_name, 'r', encoding)
        md_text = md_file.read();
        md_file.close()

        # Call function for real convert
        output = self._convert(md_text, css)

        # Write result
        # md_file_name may be: .\tests\data\somefile.md
        html_filename = self.get_file_name(md_file_name)+'.html'
        html_file = codecs.open(html_filename, 'w', HTML_ENCODING)
        html_file.write(output)
        html_file.close()

        print "'%s' file created" % (html_filename)

    def _convert(self, md_text, css = True):
        """
        Conver given text in markdown format to text in html format and
        return it. Optional boolean parameter "css" (default value is True) 
        can link stylesheet 'main.css' to html-file.
        BOM characters at the start of text determines automatically and 
        removes if exists.
        """
        import markdown2

        output = head_template

        # Process css
        css_str = ''
        if css:
            css_str = '<link rel="stylesheet" href="main.css">'
        output = output.replace('<<css>>',css_str)

        if md_text.startswith(BOM):
            md_text = md_text[1:]
            print 'remove BOM'
        text = markdown2.markdown(md_text, extras=['tables', 'wiki-tables'])
        output += text

        output += tail_template

        return output


    def get_file_name(self, full_path):
        """extract clear file name (without extention) from full path"""
        parts = full_path.split('.')
        result = parts[len(parts) - 2]
        if full_path.startswith('.'):
            result = '.' + result
        return result

    def get_args(self, argv=sys.argv[1:]):
        """ Parse command line parameters (or stub array) and return args 
        object. Valid parameters --css, --encoding and positional 
        Markdown file name.
        """
        parser = argparse.ArgumentParser(
                description = 'Convert given markdown file into HTML-file. \
                Name of HTML-file corresponds to the markdown one.')
        parser.add_argument('-css', '--css', action = 'store_true', dest = 'css', 
                help = 'Enter if you want to link your html file with main.css')
        parser.add_argument('--encoding', default = MD_ENCODING, 
                help = 'Encoding of markdown file. UTF-8 if ommit. \
                You can use cp1251, cp866 etc.')
        parser.add_argument('md_file_name', help = 'Markdown file name')

        args = parser.parse_args(argv)
        return args

    def check_md_file_name(self, md_file_name):
        """Check if given file name is not None and file extention in 
        'md', 'mdown' or 'markdown'
        """

        if md_file_name is None or not re.match(
                '.*\.md$|.*\.mdown$|.*\.markdown$',
                md_file_name, 
                re.IGNORECASE):
            return False
        return True


def main(arg_array = None):
    """
    Starter for convertor, when called from command line.
    Parameter "args" used only form unit testing.
    """
    convertor = Convertor()
    args = convertor.get_args(arg_array)
    if not convertor.check_md_file_name(args.md_file_name):
        print 'You forgot to enter markdown file name'
        sys.exit(1)
        

    convertor.convert(args.md_file_name, args.css, args.encoding)


if __name__ == '__main__':
    main()