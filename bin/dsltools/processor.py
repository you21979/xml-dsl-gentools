#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------
import os

EXT_NAME=".tmpl"
PREFIX_NAME="gen."


class Processor:

    def __init__(self, template_dir, output_dir, replace_prefix_name, encode):
        # テンプレートディレクトリ
        self.template_dir = template_dir
        # 出力ディレクトリ
        self.output_dir = output_dir
        # ファイル名につけるプリフィックス
        self.replace_prefix_name = replace_prefix_name
        # 出力文字タイプ
        self.encode_character = encode

    # -------------------------------------
    # テンプレートのスキャン
    def scan(self, func):
        # テンプレートディレクトリをスキャン
        for f in filter(lambda f : f[-len(EXT_NAME):] == EXT_NAME, os.listdir(self.template_dir)):
            # ファイル名生成
            in_fna = os.path.join(self.template_dir, f)

            out_fna = os.path.join(self.output_dir, f.replace(PREFIX_NAME, self.replace_prefix_name)[0:-len(EXT_NAME)])

            func( in_fna, out_fna )

    # -------------------------------------
    # テンプレート一覧
    def show_input_files(self):
        def printfnc(in_fna, out_fna):
            print in_fna
        self.scan(printfnc)
    # -------------------------------------
    # ジェネレートファイル一覧
    def show_output_files(self):
        def printfnc(in_fna, out_fna):
            print out_fna
        self.scan(printfnc)

    # -------------------------------------
    # ファイルの更新チェック
    def checkUpdate(self, in_fna, out_fna):
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
    def proc(self, func):
        def printfnc(in_fna, out_fna):
            # 更新時間をチェックしてジェネレートするか決める
            flag = self.checkUpdate(in_fna, out_fna)

            if flag == True:
                # ジェネレート
                print 'generate exec ' + out_fna
                func(in_fna, out_fna)
            else:
                print 'generate pass ' + out_fna
        self.scan(printfnc)


#aaaa = Processor("./hoge_tmpl", "./", "OOOO_", "utf8")
#aaaa.show_input_files()
#aaaa.show_output_files()


