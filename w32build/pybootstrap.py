#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import csv
import stat
import random
from genshi.template import NewTextTemplate
from xml.etree.ElementTree import ElementTree
import datamodel
import generator

# メイン
def main(argc,argv):
	if argc > 1:
		execfile(argv[1],globals())

main(len(sys.argv),sys.argv)

