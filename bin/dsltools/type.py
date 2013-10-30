#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------

class TypeUInt8:
    def __init__(self, name):
        self.name = name
        self.type = 'uint8'
        self.size = 1

class TypeUInt16:
    def __init__(self, name):
        self.name = name
        self.type = 'uint16'
        self.size = 2

class TypeUInt32:
    def __init__(self, name):
        self.name = name
        self.type = 'uint16'
        self.size = 4

class TypeUInt64:
    def __init__(self, name):
        self.name = name
        self.type = 'uint16'
        self.size = 8

class TypeInt8:
    def __init__(self, name):
        self.name = name
        self.type = 'int8'
        self.size = 1

class TypeInt16:
    def __init__(self, name):
        self.name = name
        self.type = 'int16'
        self.size = 2

class TypeInt32:
    def __init__(self, name):
        self.name = name
        self.type = 'int16'
        self.size = 4

class TypeInt64:
    def __init__(self, name):
        self.name = name
        self.type = 'int16'
        self.size = 8

class TypeFloat:
    def __init__(self, name):
        self.name = name
        self.type = 'float'
        self.size = 4

class TypeDouble:
    def __init__(self, name):
        self.name = name
        self.type = 'double'
        self.size = 8

class TypeByte:
    def __init__(self, name):
        self.name = name
        self.type = 'byte'
        self.size = 1

class TypeString:
    def __init__(self, name):
        self.name = name
        self.type = 'string'
        self.size = 1

class TypeStruct:
    def __init__(self, name):
        self.name = name
        self.type = 'struct'
        self.size = 0

class TypeDatabase:
    def __init__(self):
        self.database = {}
        self.add(TypeUInt8('uint8'))
        self.add(TypeUInt16('uint16'))
        self.add(TypeUInt32('uint32'))
        self.add(TypeUInt64('uint64'))
        self.add(TypeInt8('int8'))
        self.add(TypeInt16('int16'))
        self.add(TypeInt32('int32'))
        self.add(TypeInt64('int64'))
        self.add(TypeFloat('float'))
        self.add(TypeDouble('double'))
        self.add(TypeByte('byte'))
        self.add(TypeString('string'))
        self.add(TypeUInt8('bool'))
        self.add(TypeInt32('timestamp'))

    def add(self, type):
        self.database[type.name] = type

