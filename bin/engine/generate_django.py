#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from django.template import Context, Template
from django.conf import settings

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True, TEMPLATE_DIRS=())

def output(dictionary, in_file, out_file):
    # input
    fp = open(in_file, 'r')
    tmpl = Template(fp.read())
    fp.close()

    # generate
    context = Context({
        'dic' : dictionary,
        'libdir' : os.path.dirname(in_file),
    })
    return tmpl.render(context)

