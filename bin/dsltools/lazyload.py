#!/usr/bin/python
# -*- coding:utf8 -*-
import os

def load(name):
    try:
        mod = __import__(name)
    except:
        mod_list = name.split('.')
        mod = __import__('.'.join(mod_list[:-1]))

    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def scan(dir):
    ext = ".py"
    loaded = {}
    for f in filter(lambda f : f[-len(ext):] == ext, os.listdir(dir)):
        name = f[:-len(ext)]
        if name == '__init__':
            continue
        loaded[name] = load(dir + "." + name)
    return loaded
        
