#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------
from word_list import WordList

class BaseItem:
    def __init__(self):
        self.parent = None
        self.tag = ''
        self.data = {}
    def toLCamel(self,name):
        wl = WordList()
        wl.fromSnakeCase(self.data[name])
        return wl.toLCamel()
    def toUCamel(self,name):
        wl = WordList()
        wl.fromSnakeCase(self.data[name])
        return wl.toUCamel()
    def toLower(self,name):
        wl = WordList()
        wl.fromSnakeCase(self.data[name])
        return wl.toLCase()
    def toUpper(self,name):
        wl = WordList()
        wl.fromSnakeCase(self.data[name])
        return wl.toUCase()

