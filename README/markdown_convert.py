# -*- coding: utf-8 -*-
#
# markdown_converter.py
#

"""
Convert README documents to reStructured.
"""


import pypandoc


def converter(path_md_doc):
    """Convert README documents from markdown to reStructured (rst)."""

    converted = pypandoc.convert(path_md_doc, 'rst')

    # Writes converted file.
    with open('./README.rst', 'w') as outfile:
        outfile.write(converted)


if __name__ == '__main__':

    converter('./README.md')
