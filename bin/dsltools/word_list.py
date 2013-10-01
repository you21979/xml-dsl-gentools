#!/usr/bin/python
# -*- coding: utf-8 -*-

SNAKE_SEPARATOR = "_"

class WordList:
    def __init__(self):
        self.words = []

    def fromString(self, str, separator):
        if str == "":
            return
        self.fromList(str.split(separator))

    def fromSnakeCase(self, str):
        self.fromString(str, SNAKE_SEPARATOR)

    def fromSpaceSeparate(self, str):
        self.fromString(str, " ")

    def fromList(self,lists):
        self.words.extend(lists)

    def toSnakeCase(self):
        str = ""
        for word in self.words:
            if str == "":
                str = word
            else:
                str = str + SNAKE_SEPARATOR + word
        return str

    def toCapitalize(self):
        str = ""
        for word in self.words:
            str = str + word.capitalize()
        return str

    def toUCase(self):
        return self.toSnakeCase().upper()

    def toLCase(self):
        return self.toSnakeCase().lower()

    def toUCamel(self):
        return self.toCapitalize()

    def toLCamel(self):
        work = self.toCapitalize()
        if work == '':
            return work
        top = work[0].lower()
        content = work[1:-1] + work[-1]
        return top + content

