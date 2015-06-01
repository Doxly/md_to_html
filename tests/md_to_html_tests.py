# -*- coding: utf-8 -*-
from nose.tools import *
import codecs
import os

import md_to_html.mdtohtml
# from md_to_html.mdtohtml import Convertor

class md_to_html_tests(object):
    """docstring for NAME_tests"""
        
    def setup(self):
        # print "SETUP!"
        self.convertor = md_to_html.mdtohtml.Convertor()

    def teardown(self):
        # print "TEAR DOWN!"
        pass

    def test_basic(self):
        # print "I RAN!"
        arg_string = "./tests/data/test.md -css --encoding=cp1251"
        args = self.convertor.get_args(arg_string.split())
        assert_equals(args.md_file_name, "./tests/data/test.md")
        assert_equals(args.encoding, 'cp1251')

        arg_string = "./tests/data/test.md --encoding=cp1251"
        args = self.convertor.get_args(arg_string.split())
        assert_false(args.css)

    def test_get_file_name(self):
        file_name = self.convertor.get_file_name('.\\tests\data\\test.md')
        assert_equals(file_name, '.\\tests\\data\\test')

        file_name = self.convertor.get_file_name('test.markdown')
        assert_equals(file_name, 'test')

        file_name = self.convertor.get_file_name('c:/somedir/file_name.txt')
        assert_equals(file_name, 'c:/somedir/file_name')

    def test_check_md_file_name(self):
        assert_true(self.convertor.check_md_file_name('test.md'))
        assert_true(self.convertor.check_md_file_name('test.mdown'))
        assert_true(self.convertor.check_md_file_name('test.markdown'))
        assert_true(self.convertor.check_md_file_name('./test.md'))
        assert_true(self.convertor.check_md_file_name('.\\test.md'))
        assert_true(self.convertor.check_md_file_name('.\\folder\\test.md'))
        assert_true(self.convertor.check_md_file_name('./folder/test.md'))
        assert_true(self.convertor.check_md_file_name('./folder\\test.md'))

        assert_false(self.convertor.check_md_file_name('./folder\\test.bad'))
        assert_false(self.convertor.check_md_file_name(''))
        assert_false(self.convertor.check_md_file_name(None))

    def test_convert_inner(self):
        md_text = "#Some header"
        result = self.convertor._convert(md_text, True)
        # print "test_convert_inner. result = %s" % (result)
        assert_regexp_matches(result, 
            '<meta type="text/html" charset="%s">' % (
                md_to_html.mdtohtml.HTML_ENCODING))
        assert_regexp_matches(result, '<link rel="stylesheet" href="main.css">')
        assert_regexp_matches(result, '<h1>Some header</h1>')

        result = self.convertor._convert(md_text, False)
        assert_not_regexp_matches(result, '<link rel="stylesheet" href="main.css">')

    def get_text_for_file(self):
        """
        Return string containing static text in markdown format.
        Text contain headers, multi-tier lists (up to three levels), and 
        table in native markdown format (some columns has different alligment) 
        and wiki-style table.
        Some text in Russian language.
        """
        md_text = u"""# Test markdown file 1

This file used to test sript md\_to\_html.py

some data in list:

* first
* second
* third
    - inner list
    - end more second level
        + third level

This is main text. And some text in it is *selected*. And other __selection__. And one more ___selection___.

    This is code selection.

##Проверяем как работают таблицы:

заголовок 1 в две строки|Заголовок 2 с выравниванием вправо
--          |--:
Данные 1    | данные 2
еще данные  | и еще

##А теперь таблицы в стиле wiki:

||Заголовок||another header||
||some data||another data||
||and moredata||thats all||
"""
        return md_text

    def __create_md_file(self, md_file_name, 
            md_file_encoding = 'utf-8', with_bom = False):
        """
        Create cource mark-down file with some text. 
        Text contain some words in russian languige.
        File name passed in parameter. Parameter "md_file_encoding" is optional 
        with dafault value 'utf-8'. Possible values for "md_file_encoding" is
        'cp1251', 'cp886', etc.
        If "md_file_encoding" is 'utf-8' it is possible generate file with 
        started BOM bites (u'\ufeff') by passing boolean value throu "with_bom"
        parameter. Default value for "with_bom" parameter is False.
        """
        md_text = ''
        # md_file_encoding = 'utf-8'
        if with_bom & (md_file_encoding == 'utf-8'):
            md_text = md_to_html.mdtohtml.BOM
        md_text += self.get_text_for_file()
        # md_file_name = '.\\tests\data\utest.md'

        md_file = codecs.open(md_file_name, 'w', 
            md_file_encoding)
        md_file.write(md_text)
        md_file.close()
        

    def __test_convert(self, with_bom = False):
        # create test file, convert it, check generated html-file
        md_file_name = '.\\tests\utest.md'
        html_file_name = '.\\tests\utest.html'
        md_file_encoding = 'utf-8'

        self.__create_md_file(md_file_name,with_bom = with_bom)

        if os.path.isfile(html_file_name):
            os.remove(html_file_name)

        # check appearance of result html file after convertation
        assert_false(os.path.isfile(html_file_name))
        self.convertor.convert(md_file_name, None, md_file_encoding)
        assert_true(os.path.isfile(html_file_name))

        # Read content of result html file.
        html_file = codecs.open(html_file_name, 'r', 
            md_to_html.mdtohtml.HTML_ENCODING)
        html_text = html_file.read()
        html_file.close()

        # check some parts in result html file
        assert_regexp_matches(html_text, 
            r'<head>(.|\n)*</head>(.|\n)*<body>(.|\n)*</body>')
        assert_regexp_matches(html_text, 
            ur'<td align="right">данные 2</td>')

        # clear temp source and result files
        self.__remove_files([md_file_name, html_file_name])

    def __remove_files(self, files):
        for file in files:
            if os.path.isfile(file):
                os.remove(file)

    def test_convert(self):
        self.__test_convert(with_bom=False)
        self.__test_convert(with_bom=True)

    def test_main(self):
        md_file_name = '.\\tests\utest.md'
        html_file_name = '.\\tests\utest.html'
        arg_string = "./tests/utest.md -css --encoding=cp1251"
        args = arg_string.split()
        self.__create_md_file(md_file_name)
        md_to_html.mdtohtml.main(args)

        self.__remove_files([md_file_name, html_file_name])

