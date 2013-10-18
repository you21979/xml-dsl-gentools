#!/usr/bin/python
# -*- coding: utf-8 -*-
from dsltools.base_item import BaseItem
from dsltools.word_list import WordList
import sys

class Enum(BaseItem):
    def __init__(self, parent, elem):
        BaseItem.__init__(self)
        self.parent = parent
        self.params = []
        self.flags = []
        self.groups = []
        self.tag = elem.tag
        for key in elem.keys():
            self.data[key] = elem.get(key)
        self.min = sys.maxint
        self.max = -sys.maxint - 1
        self.seq = -1
        self.invalid = -1

        # フラグを使用するかどうか
        self.isflag = False
        if 'flag' in self.data:
            if self.data['flag'] == 'true':
                self.isflag = True

    def addparam(self, param):
        self.params.append(param)
        if 'value' not in param.data:
            self.seq = self.seq + 1
            param.data['value'] = str(self.seq)
        self._update(param.data['value'])
        return param

    def addflag(self, flag, value):
        self.flags.append(flag)
        flag.data['value'] = 1 << value
        return flag

    def addgroup(self, group):
        self.groups.append(group)
        return group

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

class Group(BaseItem):
    def __init__(self, parent, elem):
        BaseItem.__init__(self)
        self.parent = parent
        self.tag = elem.tag
        for key in elem.keys():
            self.data[key] = elem.get(key)

    def expand(self, func, prefix = '', suffix = ''):
        lists = []
        for item in self.data['value'].split('|'):
            word = WordList()
            word.fromSnakeCase(prefix + item + suffix)
            lists.append(func(word))

        return '|'.join(lists)

def read(root, elements):

    enum = Enum(root, elements)
    for element in elements.getiterator():
        if element.tag == "param":
            p = enum.addparam(Param(enum, element))
            if enum.isflag:
                enum.addflag(Flag(enum, element), int(p.data['value']))
        elif element.tag == "group":
            if enum.isflag:
                enum.addgroup(Group(enum, element))

    return enum


