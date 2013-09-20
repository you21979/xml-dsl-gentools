#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------
# Multi Source Code Generator for SQL
# Created by Y.Akiyama
# -----------------------------------------------------
import os
import sys
import time
import csv
import random
from genshi.template import NewTextTemplate
from xml.etree.ElementTree import ElementTree

import datamodel
import generator

# -------------------------------------
# SQLジェネレータ
# -------------------------------------
class SqlGenerator(generator.Generator21):
	# -------------------------------------
	# XML辞書データ
	# -------------------------------------
	# XML ROOT
	class XMLRoot(generator.BaseParam):
		def __init__(self):
			# 上位クラス
			self.parent = None
			# 関数の数
			self.seq = 0
			# タグ
			self.tag = ''
			# テーブルの配列
			self.table = []
			# その他オプション
			self.data = {}
			self.prefix = []
			# 必須ではないオプションを事前登録
			self.data['comment'] = ''
		# 名前を取得
		def get(self,mode):
			return datamodel.NamingConventions.Group(self.data['name'],mode)
	# -------------------------------------
	# XML Table
	class XMLTable(generator.BaseParam):
		def __init__(self):
			# 上位クラス
			self.root = None
			self.parent = None
			# 通し番号
			self.seq = -1
			# タグ
			self.tag = ''
			# その他オプション
			self.data = {}
			# パラメータ配列
			self.param = []
			# 
			self.primary = []
			# 
			self.index = []
			# 必須ではないオプションを事前登録
			self.data['comment'] = ''
		# 名前を取得
		def get(self,name,mode):
			return datamodel.NamingConventions.Group(self.data[name],mode)
	# -------------------------------------
	# XML Param
	class XMLParam(generator.BaseParam):
		def __init__(self):
			# 上位クラス
			self.root = None
			self.parent = None
			# タグ
			self.tag = ''
			# 
			self.seq = -1
			self.is_struct = False
			# その他オプション
			self.data = {}
			self.key = []
			# 必須ではないオプションを事前登録
			self.data['comment'] = ''
			self.data['opt'] = ''
		# 配列の最後以外ならセパレータを出力
		def sep(self,s):
			i = self.parent.param[-1]
			if self != i:
				return s
			return ''
		def sepPrimary(self,s):
			i = self.parent.primary[-1]
			if self != i:
				return s
			return ''
		def sepIndex(self,s):
			i = self.parent.index[-1]
			if self != i:
				return s
			return ''
		def sepKey(self,name,s):
			i = self.key[-1]
			if name != i:
				return s
			return ''
		# ユーザー定義型かどうか
		def checkType(self):
			if datamodel.LangModel.check(self.data['type']):
				self.is_struct = False
			else:
				self.is_struct = True
		# C#での型取得
		def getModelOfCS(self,mode):
			if self.is_struct:
				return datamodel.NamingConventions.Group(self.data['type'],mode)
			else:
				return datamodel.LangModel.get_csharp(self.data['type'])
		# MYSQLでの型取得
		def getModelOfMYSQL(self,mode):
			if self.is_struct:
				return datamodel.NamingConventions.Group(self.data['type'],mode)
			else:
				return datamodel.LangModel.get_mysql(self.data['type'])
		# 名前を取得
		def get(self,name,mode):
			return datamodel.NamingConventions.Group(self.data[name],mode)
	# -------------------------------------
	# XMLを解析して辞書データを作成する
	class XMLData:
		# コンストラクタ
		def __init__(self,parent):
			self.parent = parent
			self.root = SqlGenerator.XMLRoot()
			self.root.parent = self
		# root登録
		def on_orm(self,root):
			self.root.tag = root.tag
			for k in root.keys():
				self.root.data[k] = root.get(k)
			return self.root
		# CSV登録
		def on_prefix(self,root,elm,r):
			w = SqlGenerator.XMLTable()
			w.tag = elm.tag
			for k in elm.keys():
				w.data[k] = elm.get(k)
			w.parent = r
			w.root = r
			w.seq = 0
			r.prefix.append(w)
			return w
		# table登録
		def on_table(self,root,elm,r):
			w = SqlGenerator.XMLTable()
			w.tag = elm.tag
			for k in elm.keys():
				w.data[k] = elm.get(k)
			w.parent = r
			w.root = r
			w.seq = 0
			r.table.append(w)
			return w
		# パラメータ名登録
		def on_param(self,root,elm,item,f):
			w = SqlGenerator.XMLParam()
			for k in item.keys():
				w.data[k] = item.get(k)
			w.tag = item.tag
			w.parent = f
			w.root = f.root
			w.checkType()
			w.seq = f.seq
			f.seq = f.seq + 1
			f.param.append(w)
			return w
		# 登録
		def on_primary(self,root,elm,item,f):
			w = SqlGenerator.XMLParam()
			for k in item.keys():
				w.data[k] = item.get(k)
			w.tag = item.tag
			w.key = w.data['key'].split(',');
			w.type = {}
			w.parent = f
			w.root = f.root
			for p in f.param:
				for k in w.key:
					if p.data['name'] == k:
						w.type[k] = p.data['type']
			f.primary.append(w)
			return w
		# 登録
		def on_index(self,root,elm,item,f):
			w = SqlGenerator.XMLParam()
			for k in item.keys():
				w.data[k] = item.get(k)
			w.tag = item.tag
			w.key = w.data['key'].split(',');
			w.type = {}
			w.parent = f
			w.root = f.root
			for p in f.param:
				for k in w.key:
					if p.data['name'] == k:
						w.type[k] = p.data['type']
			f.index.append(w)
			return w
		# データ読み込み終了処理
		def on_complete(self):
			return
		# 定義ファイル読み込み
		def read(self,fna):
			# XMLファイル読み込み
			xml = ElementTree(file=open(fna,'r'))
			# 解析開始
			root = xml.getroot()
			r = self.on_orm(root)
			for elm in root.findall('prefix'):
				f = self.on_prefix(root,elm,r)
			# table
			for elm in root.findall('table'):
				f = self.on_table(root,elm,r)
				for item in elm.getiterator():
					if item.tag == 'param':
						self.on_param(root,elm,item,f)	
					elif item.tag == 'primary':
						self.on_primary(root,elm,item,f)	
					elif item.tag == 'index':
						self.on_index(root,elm,item,f)	
			# complete
			self.on_complete()

# -------------------------------------
# メイン
def main(argc,argv):
	opt = generator.opt_parse('sqlgen',argc,argv)
	gen = SqlGenerator(opt['config'], opt['template'], opt['output'])
	if opt['prefix'] != '':
		gen.setPrefix(opt['prefix'])
	if opt['utf8bom'] != '':
		gen.setEnc('utf8bom')
	if opt['show_output_files'] != '':
		gen.show_output_files()
	elif opt['show_input_files'] != '':
		gen.show_input_files()
	else:
		gen.main()
# -------------------------------------
main(len(sys.argv),sys.argv)
