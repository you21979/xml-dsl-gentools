#!/usr/bin/python
# -*- coding: utf-8 -*-
from dsltools.base_item import BaseItem

class Item(BaseItem):
    def __init__(self):
        BaseItem.__init__(self)


def init(root):
    item = Item()
    return item

def insert_element(root, elements):
    item = Item()
    return item

def insert_param(root, member, element):
    pass


def read(tree, tag):
    
    root = tree.getroot()
    item_root = init(root)

    for elements in root.findall(tag):
        item_member = insert_element(item_root, elements)
        for element in elements.getiterator():
            if element.tag == "param":
                insert_param(item_root, item_member, element)

    return item_root
