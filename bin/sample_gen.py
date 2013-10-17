#!/usr/bin/python
# -*- coding: utf-8 -*-
from dsltools import utils
from dsltools.processor import Processor

from optparse import OptionParser

PROGRAM_VERSION = "1.0"

def CommandOption():
    parser = OptionParser(version="%prog " + PROGRAM_VERSION)
    parser.add_option("-c", "--config", dest="config",
        help="read config file(dsl)", metavar="FILE")
    parser.add_option("-t", "--template_dir", dest="template_dir",
        help="read template directory", metavar="DIRECTORY")
    parser.add_option("-o", "--output_dir", dest="output_dir",
        help="write generate directory", metavar="DIRECTORY")
    parser.add_option("-e", "--encoding", dest="encoding",
        help="output encoding [utf8,utf8bom,sjis,euc]", metavar="ENCODING", default="utf8")
    parser.add_option("-p", "--prefix", dest="prefix", default="",
        help="additional prefix filename", metavar="STRING")
    parser.add_option("-r", "--release", dest="release", default="false",
        help="release flag", metavar="BOOL")

    return parser

def main():

    parser = CommandOption()
    (options, args) = parser.parse_args()

    try:
        xmlfile = utils.input_filename(options.config)
        encode = utils.input_select(options.encoding, ["utf8","utf8bom","sjis","euc"])
        prefix = utils.input_default(options.prefix, "")
        template_dir = utils.input_dirname(options.template_dir)
        output_dir = utils.input_dirname(options.output_dir)
        release = utils.input_bool(options.release)
    except:
        return parser.print_help()

    processor = Processor(xmlfile, template_dir, output_dir, prefix, encode)
    processor.proc()

main()


