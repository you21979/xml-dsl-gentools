#!/usr/bin/python
# -*- coding: utf-8 -*-

# 言語毎の型
class LangModel:
	# 型の存在チェック
	@staticmethod
	def check(model):
		dispatch = {
			'bool': 1,
			'int8': 1,
			'int16': 1,
			'int32': 1,
			'int64': 1,
			'uint8': 1,
			'uint16': 1,
			'uint32': 1,
			'uint64': 1,
			'string': 1,
			'binary': 1,
			'float': 1,
			'double': 1,
		}
		if dispatch.has_key(model):
			return dispatch[model]
		return 0
	# for mysql
	@staticmethod
	def get_mysql(model):
		dispatch = {
			'enum': 'int',
			'bool': 'bool',
			'int8': 'tinyint',
			'int16': 'smallint',
			'int32': 'int',
			'int64': 'bigint',
			'uint8': 'tinyint unsigned',
			'uint16': 'smallint unsigned',
			'uint32': 'int unsigned',
			'uint64': 'bigint unsigned',
			'string': 'varchar',
			'float': 'float',
			'double': 'double',
		}
		return dispatch[model]
	# for csharp
	@staticmethod
	def get_csharp(model):
		dispatch = {
			'enum': 'int',
			'bool': 'bool',
			'int8': 'sbyte',
			'int16': 'short',
			'int32': 'int',
			'int64': 'long',
			'uint8': 'byte',
			'uint16': 'ushort',
			'uint32': 'uint',
			'uint64': 'ulong',
			'string': 'string',
			'float': 'float',
			'double': 'double',
		}
		return dispatch[model]
	# for c
	@staticmethod
	def get_c(model):
		dispatch = {
			'enum': 'int32_t',
			'bool': 'char',
			'int8': 'int8_t',
			'int16': 'int16_t',
			'int32': 'int32_t',
			'int64': 'int64_t',
			'uint8': 'uint8_t',
			'uint16': 'uint16_t',
			'uint32': 'uint32_t',
			'uint64': 'uint64_t',
			'string': 'char *',
			'float': 'float',
			'double': 'double',
		}
		return dispatch[model]

# 命名規則
class NamingConventions:
	MODE_L,MODE_U,MODE_C = range(3)
	@staticmethod
	def Word(str, mode):
		if str == '':
			return ''
		dispatch = {
			NamingConventions.MODE_L: str.lower(),
			NamingConventions.MODE_U: str.upper(),
			NamingConventions.MODE_C: str.capitalize(),
		}
		return dispatch[mode]
	@staticmethod
	def Sep(mode):
		sep = {
			NamingConventions.MODE_L: '_',
			NamingConventions.MODE_U: '_',
			NamingConventions.MODE_C: '',
		}
		return sep[mode]
	@staticmethod
	def Group(str, mode):
		p = ''
		sep = NamingConventions.Sep(mode)
		for v in str.split('_'):
			if p == '':
				p = NamingConventions.Word(v,mode)
			else:
				p = p + sep +  NamingConventions.Word(v,mode)
		return p
 
# ハッシュ関数
class Hash:
	@staticmethod
	def PJW(key):
		BitsInUnsignedInt	= 4 * 8
		ThreeQuarters		= long((BitsInUnsignedInt  * 3) / 4)
		OneEighth			= long(BitsInUnsignedInt / 8)
		HighBits			= (0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth)
		value				= 0
		test				= 0
		for i in range(len(key)):
			value = (value << OneEighth) + ord(key[i])
			test = value & HighBits
			if test != 0:
				value = (( value ^ (test >> ThreeQuarters)) & (~HighBits));
		return (value & 0x7FFFFFFF)

