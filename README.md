# md_to_html

This is wrap around markdown2.py call for generate whole html file 
insteed of body content. 
## requements
* Markdown file must be in UTF-8 encoding.
* Result file would bi in UTF-8 encoding.

_Author Pichugin Viacheslav_.  
2015

##usage: 
    mdtohtml.py [-h] [-css] [--encoding ENCODING] md_file_name

Convert given markdown file into HTML-file. Name of HTML-file corresponds to
the markdown one.

positional arguments:
  md_file_name         Markdown file name

optional arguments:
  -h, --help           show this help message and exit
  -css, --css          Enter if you want to link your html file with main.css
  --encoding ENCODING  Encoding of markdown file. UTF-8 if ommit. You can use
                       cp1251, cp866 etc.