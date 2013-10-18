#!/usr/bin/python
# -*- coding: utf-8 -*-
from dsltools.base_item import BaseItem
import sys

class Enum(BaseItem):
    def __init__(self, parent, elem):
        BaseItem.__init__(self)
        self.parent = parent
        self.params = []
        self.flags = []
        self.tag = elem.tag
        for key in elem.keys():
            self.data[key] = elem.get(key)
        self.min = sys.maxint
        self.max = -sys.maxint - 1
        self.seq = -1
        self.invalid = -1

    def addparam(self, param):
        self.params.append(param)
        if 'value' not in param.data:
            self.seq = self.seq + 1
            param.data['value'] = str(self.seq)
        self._update(param.data['value'])

    def addflag(self, flag):
        self.flags.append(flag)

    def _update(self, value):
        v = int(value)
        if self.min > v:
            self.min = v
        if self.max < v:
            self.max = v
            

class Param(BaseItem):
    def __init__(self, parent, elem):
        BaseItem.__init__(self)
        self.parent = parent
        self.tag = elem.tag
        for key in elem.keys():
            self.data[key] = elem.get(key)

class Flag(BaseItem):
    def __init__(self, parent, elem):
        BaseItem.__init__(self)
        self.parent = parent
        self.tag = elem.tag
        for key in elem.keys():
            self.data[key] = elem.get(key)

def read(root, elements):

    enum = Enum(root, elements)
    for element in elements.getiterator():
        if element.tag == "param":
            enum.addparam(Param(enum, element))
        elif element.tag == "flag":
            enum.addflag(Flag(enum, element))

    return enum

