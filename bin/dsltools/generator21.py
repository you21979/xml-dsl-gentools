#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from dsltools import utils
from dsltools import lazyload
from dsltools.base_item import BaseItem
from xml.etree.ElementTree import ElementTree

class RootItem(BaseItem):
    def __init__(self):
        BaseItem.__init__(self)
        self.tag = "root"
        self.items = {}

    def add(self, name, childs):
        if name not in self.items:
            self.items[name] = []
        self.items[name].append(childs)

class Generator21:
    def __init__(self, xmlfile, template_engine = "genshi"):
        self.tree = self.readXML(xmlfile)
        switch = {
            'django': "engine.generate_django",
            'genshi': "engine.generate_genshi",
        }
        self.gen = lazyload.load(switch[template_engine])

    def readXML(self, xmlfile):
        tree = ElementTree(file=open(xmlfile, 'r'))

        root = RootItem()

        plugins = lazyload.scan("plugins")
        for plugin in plugins:
            for elements in tree.findall(plugin):
                root.add(plugin, plugins[plugin].read(root, elements))

        return root

    def output(self, in_file, out_file, encode):

        outbuff = self.gen.output(self.tree.items, in_file, out_file)

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

