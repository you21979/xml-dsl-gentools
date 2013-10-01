#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------
# Multi Source Code Generator for Constant
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
# 定数ジェネレータ
# -------------------------------------
class ConstGenerator(generator.Generator21):
    # -------------------------------------
    # XML辞書データ
    # -------------------------------------
    # XML ROOT
    class XMLRoot(generator.BaseParam):
        def __init__(self):
            # 上位クラス
            self.parent = None
            # タグ
            self.tag = ''
            # 配列
            self.const = []
            self.enum = []
            # その他オプション
            self.data = {}
            # 必須ではないオプションを事前登録
            self.data['comment'] = ''
        # 名前を取得
        def get(self,name,mode):
            return datamodel.NamingConventions.Group(self.data[name],mode)
    # -------------------------------------
    # XML Const
    class XMLConst(generator.BaseParam):
        def __init__(self):
            # 上位クラス
            self.root = None
            self.parent = None
            # タグ
            self.tag = ''
            # その他オプション
            self.data = {}
            # パラメータ配列
            self.param = []
            # 必須ではないオプションを事前登録
            self.data['comment'] = ''
        # 配列の最後以外ならセパレータを出力
        def sep(self,s):
            i = self.parent.param[-1]
            if self != i:
                return s
            return ''
        # 名前を取得
        def get(self,name,mode):
            return datamodel.NamingConventions.Group(self.data[name],mode)
        def addParam(self,param):
            self.param.append(param)
    # -------------------------------------
    # XML enum
    class XMLEnum(generator.BaseParam):
        def __init__(self):
            # 上位クラス
            self.root = None
            self.parent = None
            # タグ
            self.tag = ''
            # 通し番号
            self.seq = 0
            # エラー値
            self.invalid = -1
            # 最小値
            self.min = sys.maxint
            # 最大値
            self.max = -sys.maxint - 1
            # その他オプション
            self.data = {}
            # パラメータ配列
            self.param = []
            # フラグ配列
            self.flag = []
            # エイリアス配列
            self.alias = []
            # 固定値配列
            self.static = []
            # 必須ではないオプションを事前登録
            self.data['comment'] = ''
            # フラグのサポートデフォルト値
            self.data['flag'] = 'off'
        # 名前を取得
        def get(self,name,mode):
            return datamodel.NamingConventions.Group(self.data[name],mode)
        def addParam(self,param):
            if param.data.has_key('type') == False:
                param.data['type'] = 'int32'
            if param.data.has_key('value') == False:
                param.data['value'] = str(self.seq)
                self.seq = self.seq + 1
            else:
                self.seq = max(self.seq,int(param.data['value'])+1);
            self.max = max(self.max,int(param.data['value']))
            self.min = min(self.min,int(param.data['value']))
            self.param.append(param)
            
    # -------------------------------------
    # XML Param
    class XMLParam(generator.BaseParam):
        def __init__(self):
            # 上位クラス
            self.root = None
            self.parent = None
            # タグ
            self.tag = ''
            # ユーザー定義型かどうか
            self.is_struct = False
            # その他オプション
            self.data = {}
            # 必須ではないオプションを事前登録
            self.data['comment'] = ''
        # 配列の最後以外ならセパレータを出力
        def sep(self,s):
            i = self.parent.param[-1]
            if self != i:
                return s
            return ''
        # C#での型取得
        def getModelOfCS(self,mode):
            if self.is_struct:
                return datamodel.NamingConventions.Group(self.data['type'],mode)
            else:
                return datamodel.LangModel.get_csharp(self.data['type'])
        # AS3での型取得
        def getModelOfAS3(self,mode):
            if self.is_struct:
                return datamodel.NamingConventions.Group(self.data['type'],mode)
            else:
                return datamodel.LangModel.get_as3(self.data['type'])
        # データ取得
        def get(self,name,mode):
            return datamodel.NamingConventions.Group(self.data[name],mode)
        def getName(self,type,mode):
            dispatch = {
                0: self.data['name'],
                1: self.parent.data['name']+'_'+self.data['name'],
                2: self.parent.parent.data['name']+'_'+self.parent.data['name']+'_'+self.data['name'],
            }
            return datamodel.NamingConventions.Group(dispatch[type],mode)
    # -------------------------------------
    # XMLを解析して辞書データを作成する
    class XMLData:
        # コンストラクタ
        def __init__(self,parent):
            self.parent = parent
            self.root = ConstGenerator.XMLRoot()
            self.root.parent = self
        # プロトコル名登録
        def on_constant(self,root):
            self.root.tag = root.tag
            for k in root.keys():
                self.root.data[k] = root.get(k)
            return self.root
        # const登録
        def on_const(self,root,elm,r):
            w = ConstGenerator.XMLConst()
            w.tag = elm.tag
            for k in elm.keys():
                w.data[k] = elm.get(k)
            w.parent = r
            w.root = r
            r.const.append(w)
            return w
        # enum登録
        def on_enum(self,root,elm,r):
            w = ConstGenerator.XMLEnum()
            w.tag = elm.tag
            for k in elm.keys():
                w.data[k] = elm.get(k)
            w.parent = r
            w.root = r
            r.enum.append(w)
            return w
        # パラメータ名登録
        def on_param(self,root,elm,item,f):
            w = ConstGenerator.XMLParam()
            for k in item.keys():
                w.data[k] = item.get(k)
            w.tag = item.tag
            w.parent = f
            w.root = f.root
            f.addParam(w)
            return w
        # エイリアス名登録
        def on_param_alias(self,root,elm,item,f):
            w = ConstGenerator.XMLParam()
            for k in item.keys():
                w.data[k] = item.get(k)
            w.tag = item.tag
            w.parent = f
            w.root = f.root
            f.alias.append(w)
            return w
        # フラグ名登録
        def on_param_flag(self,root,elm,item,f):
            w = ConstGenerator.XMLParam()
            for k in item.keys():
                w.data[k] = item.get(k)
            w.tag = item.tag
            w.parent = f
            w.root = f.root
            f.flag.append(w)
            return w
        # エラー値登録
        def on_param_invalid(self,root,elm,item,f):
            w = ConstGenerator.XMLParam()
            for k in item.keys():
                w.data[k] = item.get(k)
            w.tag = item.tag
            w.parent = f
            w.root = f.root
            if w.data.has_key('value') == False:
                w.data['value'] = str(f.invalid)
            f.static.append(w)
            return w
        # サイズ登録
        def on_param_sizeof(self,root,elm,item,f):
            w = ConstGenerator.XMLParam()
            for k in item.keys():
                w.data[k] = item.get(k)
            w.tag = item.tag
            w.parent = f
            w.root = f.root
            if w.data.has_key('value') == False:
                w.data['value'] = str(f.seq)
            f.static.append(w)
            return w
        # 最大値登録
        def on_param_max(self,root,elm,item,f):
            w = ConstGenerator.XMLParam()
            for k in item.keys():
                w.data[k] = item.get(k)
            w.tag = item.tag
            w.parent = f
            w.root = f.root
            if w.data.has_key('value') == False:
                w.data['value'] = str(f.max)
            f.static.append(w)
            return w
        # 最小値登録
        def on_param_min(self,root,elm,item,f):
            w = ConstGenerator.XMLParam()
            for k in item.keys():
                w.data[k] = item.get(k)
            w.tag = item.tag
            w.parent = f
            w.root = f.root
            if w.data.has_key('value') == False:
                w.data['value'] = str(f.min)
            f.static.append(w)
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
            r = self.on_constant(root)
            # const
            for elm in root.findall('const'):
                f = self.on_const(root,elm,r)
                for item in elm.getiterator():
                    if item.tag == 'param':
                        self.on_param(root,elm,item,f)    
            # enum
            for elm in root.findall('enum'):
                f = self.on_enum(root,elm,r)
                for item in elm.getiterator():
                    if item.tag == 'param':
                        self.on_param(root,elm,item,f)    
                    elif item.tag == 'alias':
                        self.on_param_alias(root,elm,item,f)    
                    elif item.tag == 'flag':
                        self.on_param_flag(root,elm,item,f)    
                    elif item.tag == 'min':
                        self.on_param_min(root,elm,item,f)    
                    elif item.tag == 'max':
                        self.on_param_max(root,elm,item,f)    
                    elif item.tag == 'invalid':
                        self.on_param_invalid(root,elm,item,f)    
                    elif item.tag == 'sizeof':
                        self.on_param_sizeof(root,elm,item,f)    
            # complete
            self.on_complete()

# -------------------------------------
# メイン
def main(argc,argv):
    opt = generator.opt_parse('constgen',argc,argv)
    gen = ConstGenerator(opt['config'], opt['template'], opt['output'])
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
