#!/usr/bin/python
# -*- coding: utf-8 -*-
from dsltools.base_item import BaseItem

class Enum(BaseItem):
    def __init__(self, parent, elem):
        BaseItem.__init__(self)
        self.parent = parent
        self.params = []
        self.tag = elem.tag
        for key in elem.keys():
            self.data[key] = elem.get(key)
    def add(self, param):
        self.params.append(param)

class Param(BaseItem):
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
            enum.add(Param(enum, element))

    return enum

