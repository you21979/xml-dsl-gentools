#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------
import word_list

class BaseItem:
    def __init__(self):
        self.parent = None
        self.tag = ''
        self.data = {}
    def toLCamel(self,name):
        wl = dsltools.word_list()
        wl.fromSnakeCase(self.data[name])
        return wl.toLCamel()
    def toUCamel(self,name):
        wl = dsltools.word_list()
        wl.fromSnakeCase(self.data[name])
        return wl.toUCamel()
    def toLower(self,name):
        wl = dsltools.word_list()
        wl.fromSnakeCase(self.data[name])
        return wl.toLCase()
    def toUpper(self,name):
        wl = dsltools.word_list()
        wl.fromSnakeCase(self.data[name])
        return wl.toUCase()

