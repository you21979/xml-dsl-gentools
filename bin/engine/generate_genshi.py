#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from genshi.template import NewTextTemplate

def output(dictionary, in_file, out_file):
    # input
    fp = open(in_file, 'r')
    tmpl = NewTextTemplate(fp.read())
    fp.close()
    # generate
    return tmpl.generate(
        dic = dictionary,
        langdir = os.path.dirname(in_file) + "/../langlib",
        libdir = os.path.dirname(in_file)
    ).render('text')

