#!/usr/bin/python
# -*- coding: utf-8 -*-

def input_default(value, default):
    if value:
        return value
    else:
        return default

def input_select(value, select_list):
    for item in select_list:
        if item == value:
            return item
    raise

def input_filename(value):
    v = input_default(value, "")
    if v == "":
        raise
    return v

def input_dirname(value):
    v = input_default(value, "")
    if v == "":
        raise
    return v

def input_bool(value):
    v = input_default(value, "false").lower()
    if v == "true":
        return True
    elif v == "false":
        return False
    else:
        raise

def output_utf8bom_header(fp):
    fp.write('\xef\xbb\xbf')


