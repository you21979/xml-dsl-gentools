#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------
# Multi Source Code Generator for Network Protocol
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
# プロトコルジェネレータ
# -------------------------------------
class ProtocolGenerator(generator.Generator21):
    # -------------------------------------
    # ユニークハッシュ生成
    # -------------------------------------
    class UniqHash:
        def __init__(self,seed,max):
            random.seed(seed)
            self.masterkey = str(random.randint(1,100000000))
            self.max = max
            self.half = max / 2
            self.table = {}
        def get(self,val):
            h = datamodel.Hash.PJW(self.masterkey + val + self.masterkey) % self.max + 1
            count = 0
            while True:
                if self.table.has_key(h + count) == False:
                    self.table[h + count] = val
                    return h + count
                else:
                    if self.table[h + count] == val:
                        return -1
                    # 衝突したら一個ずらしてうまくいくかためす
                    if self.half > h:
                        count = count + 1
                    else:
                        count = count - 1
                    if h + count >= max:
                        print "error count max"
                        sys.exit(-1)
                    elif h + count < 0:
                        print "error count max"
                        sys.exit(-1)
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
            # 関数の配列
            self.func = []
            # 構造体の配列
            self.struct = []
            self.struct_hash = {}
            # その他オプション
            self.data = {}
            # 必須ではないオプションを事前登録
            self.data['comment'] = ''
            # RPC値のバイトサイズ
            self.data['rpcbytesize'] = 2
            # デバッグオプション
            self.data['debug'] = 'true'
        # 名前を取得
        def get(self,name,mode):
            return datamodel.NamingConventions.Group(self.data[name],mode)
        # ランダムのシードを取得
        def getRandomSeed(self):
            seed = datamodel.Hash.PJW(self.data['name']) ^ int(self.data['id']) ^ int(self.data['major'])
            return seed
    # -------------------------------------
    # XML Struct
    class XMLStruct(generator.BaseParam):
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
            # コードヒント用のデータ
            self.codehint = []
            # 必須ではないオプションを事前登録
            self.data['comment'] = ''    # コメント
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
    # XML Func
    class XMLFunc(generator.BaseParam):
        def __init__(self):
            # 上位クラス
            self.root = None
            self.parent = None
            # 通し番号
            self.seq = -1
            # ハッシュ値
            self.hash = -1
            # タグ
            self.tag = ''
            # その他オプション
            self.data = {}
            # パラメータ配列
            self.param = []
            # コードヒント用のデータ
            self.codehint = []
            # 必須ではないオプションを事前登録
            self.data['release'] = 'true'    # リリース
            self.data['comment'] = ''    # コメント
            self.data['id'] = ''        # RPC ID
        # 名前を取得
        def get(self,name,mode):
            return datamodel.NamingConventions.Group(self.data[name],mode)
        # RPC値を取得
        def getRPC(self,isRandomize):
            if isRandomize:
                return self.hash
            else:
                return self.seq
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
            # 配列かどうか
            self.arrayinfo = []
            # その他オプション
            self.data = {}
            # 必須ではないオプションを事前登録
            self.data['comment'] = ''    # コメント
            self.data['array'] = ''     # 配列最大数
            self.data['len'] = '256'    # 最大文字数
        # 配列の最後以外ならセパレータを出力
        def sep(self,s):
            i = self.parent.param[-1]
            if self != i:
                return s
            return ''
        # 内部データ更新
        def update(self):
            # 構造体かどうか判定
            # プリミティブ型かどうか
            if datamodel.LangModel.check(self.data['type']):
                self.is_struct = False
            else:
                # 構造体かどうか
                if self.root.struct_hash.has_key(self.data['type']):
                    self.is_struct = True
                else:
                    # 把握していない定義
                    self.is_struct = False
            # 配列情報
            if self.data['array'] != '' :
                self.arrayinfo = self.data['array'].split(',',5) # 5次元配列まで
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
    # XMLを解析して辞書データを作成する
    class XMLData:
        # コンストラクタ
        def __init__(self,parent):
            self.parent = parent
            self.root = ProtocolGenerator.XMLRoot()
            self.root.parent = self
        # プロトコル名登録
        def on_proto(self,root):
            self.root.tag = root.tag
            for k in root.keys():
                self.root.data[k] = root.get(k)
            return self.root
        # 構造体登録
        def on_struct(self,root,elm,r):
            w = ProtocolGenerator.XMLStruct()
            w.tag = elm.tag
            for k in elm.keys():
                w.data[k] = elm.get(k)
            w.parent = r
            w.root = r
            r.struct_hash[w.data['name']] = len(r.struct)
            r.struct.append(w)
            return w
        # 関数名登録
        def on_func(self,root,elm,r):
            w = ProtocolGenerator.XMLFunc()
            w.tag = elm.tag
            for k in elm.keys():
                w.data[k] = elm.get(k)
            w.parent = r
            w.root = r
            w.seq = r.seq
            if w.data['id'] == '':
                w.data['id'] = r.seq
            r.seq = r.seq + 1
            r.func.append(w)
            return w
        # パラメータ名登録
        def on_param(self,root,elm,item,f):
            w = ProtocolGenerator.XMLParam()
            for k in item.keys():
                w.data[k] = item.get(k)
            w.tag = item.tag
            w.parent = f
            w.root = f.root
            w.update()
            f.param.append(w)
            return w
        # パラメータ名登録
        def on_codehint(self,root,elm,item,f):
            w = ProtocolGenerator.XMLParam()
            for k in item.keys():
                w.data[k] = item.get(k)
            w.tag = item.tag
            w.parent = f
            w.root = f.root
            f.codehint.append(w)
            return w
        # データ読み込み終了処理
        def on_complete(self):
            # 条件が同じなら同じ値が出るようにシードをセットする
            seed = self.root.getRandomSeed()
            max = pow(2,self.root.data['rpcbytesize']*8)
            h = ProtocolGenerator.UniqHash(seed, max)
            # RPC値をシャッフルする
            for s in self.root.func:
                v = h.get(s.data['id'])
                if v == -1:
                    print "error same id"
                    sys.exit(-1)
                s.hash = v
        # 定義ファイル読み込み
        def read(self,fna):
            # XMLファイル読み込み
            xml = ElementTree(file=open(fna,'r'))
            # 解析開始
            root = xml.getroot()
            r = self.on_proto(root)
            # struct
            for elm in root.findall('struct'):
                f = self.on_struct(root,elm,r)
                for item in elm.getiterator():
                    if item.tag == 'param':
                        self.on_param(root,elm,item,f)    
                    elif item.tag == 'codehint':
                        self.on_codehint(root,elm,item,f)    
            # func
            for elm in root.findall('func'):
                if self.parent.isRelease == True:
                    if elm.get('release') == 'false':
                        print "Release Mode SKIP Func: " + elm.get('name')
                        continue
                
                f = self.on_func(root,elm,r)
                for item in elm.getiterator():
                    if item.tag == 'param':
                        self.on_param(root,elm,item,f)    
                    elif item.tag == 'codehint':
                        self.on_codehint(root,elm,item,f)    
            # complete
            self.on_complete()
# -------------------------------------
# メイン
def main(argc,argv):
    opt = generator.opt_parse('protogen',argc,argv)
    gen = ProtocolGenerator(opt['config'], opt['template'], opt['output'])
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
main(len(sys.argv),sys.argv)

            

