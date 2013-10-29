#!/usr/bin/python
# -*- coding: utf-8 -*-
from dsltools.base_item import BaseItem

class Struct(BaseItem):
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
        self.is_array = False
        self.is_struct = False
        for key in elem.keys():
            self.data[key] = elem.get(key)
        if 'array' in self.data:
            self.is_array = True
        if 'array' not in self.data:
            self.data['array'] = ''

class ParamInteger(Param):
    def __init__(self, parent, elem):
        Param.__init__(self, parent, elem)
        if 'validate' not in self.data:
            self.data['validate'] = ''
        if 'value' not in self.data:
            self.data['value'] = '0';

class ParamFloat(Param):
    def __init__(self, parent, elem):
        Param.__init__(self, parent, elem)
        if 'value' not in self.data:
            self.data['value'] = '0.0';

class ParamString(Param):
    def __init__(self, parent, elem):
        Param.__init__(self, parent, elem)
        if 'length' not in self.data:
            self.data['length'] = '256'
        if 'value' not in self.data:
            self.data['value'] = '';

class ParamStruct(Param):
    def __init__(self, parent, elem):
        Param.__init__(self, parent, elem)
        self.is_struct = 'struct'
        if 'value' not in self.data:
            self.data['value'] = '';

TYPE_DISPATCH = {
    'uint8' : ParamInteger,
    'uint16' : ParamInteger,
    'uint32' : ParamInteger,
    'uint64' : ParamInteger,
    'int8' : ParamInteger,
    'int16' : ParamInteger,
    'int32' : ParamInteger,
    'int64' : ParamInteger,
    'float' : ParamFloat,
    'double' : ParamFloat,
    'string' : ParamString,
}

def read(root, elements):
    s = Struct(root, elements)
    TYPE_DISPATCH[s.data['name']] = ParamStruct
    for element in elements.getiterator():
        if element.tag == "param":
            param = TYPE_DISPATCH[element.get('type')](s, element)
            s.add(param)

    return s

