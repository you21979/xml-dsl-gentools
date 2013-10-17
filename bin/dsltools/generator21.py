#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from dsltools import utils
from dsltools import lazyload
from dsltools.base_item import BaseItem
from xml.etree.ElementTree import ElementTree
#from genshi.template import NewTextTemplate
from django.template import loader, RequestContext

from optparse import OptionParser

PROGRAM_VERSION = "1.0"

class Item(BaseItem):
    def __init__(self):
        BaseItem.__init__(self)

class Generator21:
    def __init__(self, xmlfile):
        self.tree = self.readXML(xmlfile)

    def readXML(self, xmlfile):
        tree = ElementTree(file=open(xmlfile, 'r'))

        itemroot = Item()

        plugins = lazyload.scan("plugins")
        for plugin in plugins:
            plugin.read(tree)

        #root = tree.getroot()
        #itemroot.tag = root.tag
        #print root
        
        #for element in root.findall('struct'):
        #    for item in element.getiterator():
        #        break
        return itemroot

    def output(self, in_file, out_file, encode):
        # input
        fp = open(in_file, 'r')
#        tmpl = NewTextTemplate(fp.read())
        fp.close()

        # generate
 #       outbuff = tmpl.generate(
 #           xml = self.tree,
 #           libdir = os.path.dirname(in_file)
 #       ).render('text')
        outbuff = "aa"

        # output
        fp = open(out_file, 'w')
        switch = {
            'utf8': output_utf8,
            'sjis': output_sjis,
            'euc': output_euc,
            'utf8bom': output_utf8bom,
        }
        switch[encode](fp, outbuff)
        fp.close()

def output_utf8(fp, buff):
    fp.write(buff)
    
def output_utf8bom(fp, buff):
    utils.output_utf8bom_header(fp)
    output_utf8(fp, buff)

def output_sjis(fp, buff):
    fp.write(buff)

def output_euc(fp, buff):
    fp.write(buff)

