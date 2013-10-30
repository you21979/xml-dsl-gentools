#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------
from word_list import WordList

class BaseItem:
    def __init__(self):
        self.parent = None
        self.tag = ''
        self.data = {}
        self.is_array = False
        self.data['comment'] = ''
    def toLCamel(self, name, prefix = '', suffix = ''):
        wl = WordList()
        wl.fromSnakeCase(prefix + self.data[name] + suffix)
        return wl.toLCamel()
    def toUCamel(self, name, prefix = '', suffix = ''):
        wl = WordList()
        wl.fromSnakeCase(prefix + self.data[name] + suffix)
        return wl.toUCamel()
    def toLower(self, name, prefix = '', suffix = ''):
        wl = WordList()
        wl.fromSnakeCase(prefix + self.data[name] + suffix)
        return wl.toLCase()
    def toUpper(self, name, prefix = '', suffix = ''):
        wl = WordList()
        wl.fromSnakeCase(prefix + self.data[name] + suffix)
        return wl.toUCase()

