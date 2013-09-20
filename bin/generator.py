#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------
# Multi Source Code Generator [Generator21]
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

# XML格納用パラメータ
class BaseParam:
	def __init__(self):
		# 上位クラス
		self.parent = None
		# タグ
		self.tag = ''
		# データ
		self.data = {}
		# 必須ではないオプションを事前登録
		self.data['comment'] = ''
	# -----------------
	# lower camel case
	# -----------------
	def toLCamel(self,name):
		work = datamodel.NamingConventions.Group(self.data[name],datamodel.NamingConventions.MODE_C)
		if work == '':
			return work
		top = work[0].lower()
		content = work[1:-1] + work[-1]
		return top + content
	# -----------------
	# upper camel case
	# -----------------
	def toUCamel(self,name):
		return datamodel.NamingConventions.Group(self.data[name],datamodel.NamingConventions.MODE_C)
	# -----------------
	# upper
	# -----------------
	def toUpper(self,name):
		return datamodel.NamingConventions.Group(self.data[name],datamodel.NamingConventions.MODE_U)
	# -----------------
	# lower
	# -----------------
	def toLower(self,name):
		return datamodel.NamingConventions.Group(self.data[name],datamodel.NamingConventions.MODE_L)

# -------------------------------------
# ジェネレータ
# -------------------------------------
class Generator21:
	class XMLData:
		def __init__(self,parent):
			return
		def read(self,fna):
			return
	# -------------------------------------
	# ジェネレータ
	# -------------------------------------
	# コンストラクタ
	def __init__(self,def_file,template_dir,output_dir):
		# 定義ファイル
		self.def_file = def_file
		# テンプレートディレクトリ
		self.template_dir = template_dir
		# 出力ディレクトリ
		self.output_dir = output_dir
		# ファイル名につけるプリフィックス
		self.prefix = ''
		# 出力文字タイプ
		self.enc = 'utf8'
		# XML辞書
		self.XML = self.XMLData(self)
		# リリースフラグ
		self.isRelease = False
	# -------------------------------------
	# プレフィックス登録
	def setPrefix(self,name):
		self.prefix = name
	# -------------------------------------
	# エンコードを指定
	def setEnc(self,name):
		self.enc = name
	# -------------------------------------
	# リリースかどうか
	def setRelease(self,name):
		if name == "1":
			self.isRelease = True
	# -------------------------------------
	# ジェネレート処理
	def gen(self,in_file,out_file):
		# input
		fp = open(in_file,'r')
		tmpl = NewTextTemplate(fp.read())
		fp.close()
		# generate
		outbuff = tmpl.generate(xml=self.XML,lib=os.path.join(self.template_dir,'lib.inc')).render('text')
		# output
		fp = open(out_file,'w')
		if self.enc == 'utf8bom':
			fp.write('\xef\xbb\xbf')
		fp.write(outbuff)
		fp.close()
	# -------------------------------------
	# ファイルの更新チェック
	def checkUpdate(self,in_fna,out_fna):
		flag = False
		try:
			out_st = os.stat(out_fna)
			in_st = os.stat(in_fna)
			def_st = os.stat(self.def_file)
			if out_st.st_mtime < def_st.st_mtime:
				flag = True
			elif out_st.st_mtime < in_st.st_mtime:
				flag = True
			else:
				flag = False
		except OSError:
			flag = True
		return flag
	# -------------------------------------
	# テンプレートディレクトリから一括でジェネレート
	def proc(self):
		# テンプレートディレクトリをスキャン
		for f in os.listdir(self.template_dir):
			try:
				# 拡張子.tmpl以外を実行しない
				i = f.rindex('.tmpl')
			except ValueError:
				continue
			# 入力ファイル名生成
			in_fna = os.path.join(self.template_dir, f)

			# 出力ファイル名生成
			out_fna = os.path.join(self.output_dir, f[:i].replace('gen.',self.prefix))

			# 更新時間をチェックしてジェネレートするか決める
			flag = self.checkUpdate(in_fna,out_fna)

			if flag == True:
				# ジェネレート
				print 'generate exec ' + out_fna
				self.gen(in_fna, out_fna)
			else:
				print 'generate pass ' + out_fna
	# -------------------------------------
	# デバッグ
	def debug(self):
		for s in self.XML.root.table:
			print("+"+s.data['name']+":seq="+str(s.seq))
			for p in s.param:
				print(" :"+p.data['name']+":seq="+str(p.seq))
	# -------------------------------------
	# メインフロー
	def main(self):
		self.XML.read(self.def_file)
		#self.debug()
		self.proc()
	# -------------------------------------
	# テンプレート一覧
	def show_input_files(self):
		# テンプレートディレクトリをスキャン
		for f in os.listdir(self.template_dir):
			try:
				# 拡張子.tmpl以外を実行しない
				i = f.rindex('.tmpl')
			except ValueError:
				continue
			# 入力ファイル名生成
			in_fna = os.path.join(self.template_dir, f)
			print(in_fna)
	# -------------------------------------
	# ジェネレートファイル一覧
	def show_output_files(self):
		# テンプレートディレクトリをスキャン
		for f in os.listdir(self.template_dir):
			try:
				# 拡張子.tmpl以外を実行しない
				i = f.rindex('.tmpl')
			except ValueError:
				continue
			# 出力ファイル名生成
			out_fna = os.path.join(self.output_dir, f[:i].replace('gen.',self.prefix))
			print(out_fna)

# コマンドオプションの説明
def opt_show(name):
	print 'exsample:'
	print ' '+name+'.py -c define.xml -t template_dir -o output_dir'
	print ' '+name+'.py -c define.xml -t template_dir -o output_dir --prefix hoge'
	print ' '+name+'.py -c define.xml -t template_dir -o output_dir --show_output_files 1'
	print ' '+name+'.py -c define.xml -t template_dir -o output_dir --show_input_files 1'
	print ' '+name+'.py -c define.xml -t template_dir -o output_dir --utf8bom 1'
# コマンドオプションの解析
def opt_parse(name,argc,argv):
	opt = {};
	mustconf = { # 必須オプション
		'-c': 'config',
		'-t': 'template',
		'-o': 'output',
	}
	optconf = { # オプション
		'--release': 'release',
		'--prefix': 'prefix',
		'--show_output_files': 'show_output_files',
		'--show_input_files': 'show_input_files',
		'--utf8bom': 'utf8bom',
	}
	# 必須オプションの取得
	key = '';
	for v in argv:
		if mustconf.has_key(v):
			key = v
		else:
			if key != '':
				opt[mustconf[key]] = v
				key = ''
	for k in mustconf:
		if opt.has_key(mustconf[k]):
			continue
		else:
			opt_show(name)
			sys.exit(-1)
	# オプションコンフィグの取得 
	key = '';
	for k in optconf:
		opt[optconf[k]] = '' # 初期化
	for v in argv:
		if optconf.has_key(v):
			key = v
		else:
			if key != '':
				opt[optconf[key]] = v
				key = ''
	return opt
# -------------------------------------
# メイン
def main(argc,argv):
	opt = opt_parse('gen21',argc,argv)
	gen = Generator21(opt['config'], opt['template'], opt['output'])
	if opt['prefix'] != '':
		gen.setPrefix(opt['prefix'])
	if opt['utf8bom'] != '':
		gen.setEnc('utf8bom')
	if opt['release'] != '':
		gen.setRelease(opt['release'])
	if opt['show_output_files'] != '':
		gen.show_output_files()
	elif opt['show_input_files'] != '':
		gen.show_input_files()
	else:
		gen.main()
# -------------------------------------
#main(len(sys.argv),sys.argv)
