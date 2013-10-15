#!/usr/bin/python
# -*- coding: utf-8 -*-

def input_default(value, default):
    if value:
        return value
    else:
        return default

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

