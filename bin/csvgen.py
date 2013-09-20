#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------
# Multi Source Code Generator for Csv Reader
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
# CSVReaderジェネレータ
# -------------------------------------
class CsvGenerator(generator.Generator21):
	# -------------------------------------
	# XML辞書データ
	# -------------------------------------
	# XML ROOT
	class XMLRoot(generator.BaseParam):
		def __init__(self):
			generator.BaseParam.__init__(self)
			# 関数の数
			self.seq = 0
			# テーブルの配列
			self.table = []
			# インポートの配列
			self.prefix = []
			# 必須ではないオプションを事前登録
		# 名前を取得
		def get(self,mode):
			return datamodel.NamingConventions.Group(self.data['name'],mode)
	# -------------------------------------
	# XML Table
	class XMLTable(generator.BaseParam):
		def __init__(self):
			generator.BaseParam.__init__(self)
			# 上位クラス
			self.root = None
			# 通し番号
			self.seq = -1
			# パラメータ配列
			self.param = []
			# ファイル名
			self.file = []
			# VIEW名
			self.view = []
			# 必須ではないオプションを事前登録
			self.data['skipcount'] = '1'
			self.data['skipmark'] = '#'
		# 名前を取得
		def get(self,name,mode):
			return datamodel.NamingConventions.Group(self.data[name],mode)
	# -------------------------------------
	# XML Param
	class XMLParam(generator.BaseParam):
		def __init__(self):
			generator.BaseParam.__init__(self)
			# 上位クラス
			self.root = None
			# 
			self.seq = -1
			# ユーザー定義型かどうか
			self.is_struct = False
			# 必須ではないオプションを事前登録
			self.data['array'] = '' # 配列
			self.data['colspan'] = '1' # カラム連結
			self.colspan = [] # 配列位置記憶
		# 配列の最後以外ならセパレータを出力
		def sep(self,s):
			i = self.parent.param[-1]
			if self != i:
				return s
			return ''
		# 配列かどうか
		def checkArray(self):
			for i in range(int(self.data['colspan'])):
				self.colspan.append(i);
		# C#での型取得
		def getModelOfCS(self,mode):
			if self.is_struct:
				return datamodel.NamingConventions.Group(self.data['type'],mode)
			else:
				return datamodel.LangModel.get_csharp(self.data['type'])
		# 名前を取得
		def get(self,name,mode):
			return datamodel.NamingConventions.Group(self.data[name],mode)
	# -------------------------------------
	# XML VIEW
	class XMLView(generator.BaseParam):
		def __init__(self):
			generator.BaseParam.__init__(self)
			# 上位クラス
			self.root = None
			# その他オプション
			self.key = []
			# 必須ではないオプションを事前登録
		# 配列の最後以外ならセパレータを出力
		def sep(self,s):
			i = self.parent.param[-1]
			if self != i:
				return s
			return ''
		# 名前を取得
		def get(self,name,mode):
			return datamodel.NamingConventions.Group(self.data[name],mode)
	# -------------------------------------
	# XML VIEW
	class XMLHash(generator.BaseParam):
		def __init__(self):
			generator.BaseParam.__init__(self)
			# 上位クラス
			self.root = None
			# 必須ではないオプションを事前登録
		# 配列の最後以外ならセパレータを出力
		def sep(self,s):
			i = self.parent.key[-1]
			if self != i:
				return s
			return ''
		# 名前を取得
		def get(self,name,mode):
			return datamodel.NamingConventions.Group(self.data[name],mode)
	# -------------------------------------
	# XMLを解析して辞書データを作成する
	class XMLData:
		# コンストラクタ
		def __init__(self,parent):
			self.parent = parent
			self.root = CsvGenerator.XMLRoot()
			self.root.parent = self
		# root登録
		def on_csv(self,root):
			self.root.tag = root.tag
			for k in root.keys():
				self.root.data[k] = root.get(k)
			return self.root
		# CSV登録
		def on_prefix(self,root,elm,r):
			w = CsvGenerator.XMLTable()
			w.tag = elm.tag
			for k in elm.keys():
				w.data[k] = elm.get(k)
			w.parent = r
			w.root = r
			w.seq = 0
			r.prefix.append(w)
			return w
		# CSV登録
		def on_table(self,root,elm,r):
			w = CsvGenerator.XMLTable()
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
			w = CsvGenerator.XMLParam()
			for k in item.keys():
				w.data[k] = item.get(k)
			w.tag = item.tag
			w.parent = f
			w.root = f.root
			w.checkArray()
			w.seq = f.seq
			f.seq = f.seq + int(w.data["colspan"])
			f.param.append(w)
			return w
		# ファイル名登録
		def on_file(self,root,elm,item,f):
			w = CsvGenerator.XMLParam()
			for k in item.keys():
				w.data[k] = item.get(k)
			w.tag = item.tag
			w.parent = f
			w.root = f.root
			f.file.append(w)
			return w
		# VEIW名登録
		def on_view(self,root,elm,item,f):
			w = CsvGenerator.XMLView()
			for k in item.keys():
				w.data[k] = item.get(k)
			w.tag = item.tag
			w.parent = f
			w.root = f.root
			f.view.append(w)
			for m in item.getiterator():
				if m.tag == 'hash':
					h = CsvGenerator.XMLHash()
					for k in m.keys():
						h.data[k] = m.get(k)
					h.tag = item.tag
					h.parent = w
					w.key.append(h)
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
			r = self.on_csv(root)
			for elm in root.findall('prefix'):
				f = self.on_prefix(root,elm,r)
			# table
			for elm in root.findall('table'):
				f = self.on_table(root,elm,r)
				for item in elm.getiterator():
					if item.tag == 'param':
						self.on_param(root,elm,item,f)
					elif item.tag == 'file':
						self.on_file(root,elm,item,f)
					elif item.tag == 'view':
						self.on_view(root,elm,item,f)
			# complete
			self.on_complete()

# -------------------------------------
# メイン
def main(argc,argv):
	opt = generator.opt_parse('csvgen',argc,argv)
	gen = CsvGenerator(opt['config'], opt['template'], opt['output'])
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

			

