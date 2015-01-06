# coding: utf-8
import CONSTS
import fnmatch
import re
import logging

DEBUG_LEN = 0
#logging.basicConfig(level=logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)

class Parser:
	f = None

	def __init__(self, filename):
		self.f = open(filename, 'r')
	
	def __del__(self):
		if self.f:
			self.f.close()
	
	def secure_seek(self, pos, mode):
		# not implemented
		self.f.seek(pos, mode)
	
	def secure_read(self, size):
		# not implemented
		return self.f.read(size)

	def is_split_char_for_method_name(self, c):
		return c == ' ' or c == '\t' or c == '\n' or c == '\r'

	def is_allow_throw_char(self, c):
		return re.match("[A-Za-z0-9, \t\n\r]", c)
	
	def seek_to_char(self, c, cond = None):
		while True:
			tmp = self.secure_read(1)
			if not tmp:
				return False
			elif tmp == c:
				return self.f.tell()
			elif cond and cond(tmp):
				return False
	
	# lambda つかえばこれいらないかも
	def reverse_seek_to_char(self, c):
		while True:
			if 2 <= self.f.tell():
				self.secure_seek(-2, 1)
				tmp = f.secure_read(1)
				if not tmp:
					break
				if tmp == c:
					break
			else:
				break
	
	def reverse_seek_to_cond(self, cond):
		while True:
			if 2 <= self.f.tell():
				self.secure_seek(-2, 1)
				tmp = self.secure_read(1)
				if not tmp:
					break
				elif cond(tmp):
					break
			else:
				break
	
	# イテレータが開き括弧の1個あとを前提としているのは少し不親切かも
	def jump_to_close(self, open_mark, close_mark):
		begin = self.f.tell()
		opened = 1
		while opened > 0:
			c = self.secure_read(1)
			if not c:
				self.secure_seek(begin)
				logging.error("error in jump_to_close !!!")
				logging.error(f.secure_read(100))
				exit(-1)
			elif c == '/':
				if self.secure_read(1) == '/':
					c2 = None
					while c2 != '\r' and c2 != '\n':
						c2 = self.secure_read(1)
				else:
					pass
			elif c == open_mark:
				around_open = self.secure_read(DEBUG_LEN)
				# 戻るときはreadの最大値を考慮した戻り方が必要
				self.secure_seek(-1 * DEBUG_LEN, 1)
				logging.debug("opened")
				logging.debug(around_open)
				opened += 1
			elif c == close_mark:
				around_close = self.secure_read(DEBUG_LEN)
				# 戻るときはreadの最大値を考慮した戻り方が必要
				self.secure_seek(-1 * DEBUG_LEN, 1)
				logging.debug("closed")
				logging.debug(around_close)
				opened -= 1
	
	def find_methods(self):
		methods_content = []
		while True:
			to_open = None
			to_close = None
			to_big_open = None

			while not to_big_open:
				to_open = self.seek_to_char('(')
				to_close = self.seek_to_char(')')
				to_big_open = self.seek_to_char('{', (lambda c: not self.is_allow_throw_char(c)))
				if not to_open and not to_close and not to_big_open:
					break

			# 小括弧、波括弧のいずれかがファイルから見つからなくなったら終了
			if not to_open or not to_close or not to_big_open:
				break

			self.secure_seek(to_close, 0)
			c_to_big_o = None

			if to_big_open - to_close > 1:
				c_to_big_o = self.secure_read(to_big_open - to_close - 1)
				c_to_big_o = c_to_big_o.translate(None, ' \r\n\t')
			if not c_to_big_o or re.match("throws[A-Za-z0-9,]*", c_to_big_o):
				#logging.debug("small parenthesis to big parenthesis: " + c_to_big_o)
				self.secure_seek(to_open -1, 0)
				self.secure_seek(-1, 1)
				if self.is_split_char_for_method_name(self.secure_read(1)):
					self.secure_seek(-1, 1)
					# 1個目の区切り文字を飛ばす
					self.reverse_seek_to_cond(self.is_split_char_for_method_name)
				# メソッド名の先頭に移動
				self.reverse_seek_to_cond(self.is_split_char_for_method_name)

				methodname = ''
				c = ' '
				while c != ')':
					c = self.secure_read(1)
					methodname += c

				# 波括弧に移動するところまでイテレータを移動
				self.secure_seek(to_big_open, 0)
				self.jump_to_close('{', '}')
				to_big_close = self.f.tell()
				self.secure_seek(to_big_open, 0)
				logging.debug("methodname: " + methodname.translate(None, ' \r\n\t').replace('Type', ''))
				method_content = self.secure_read(to_big_close - to_big_open - 1)
				methods_content.append({
					'name': methodname.translate(None, ' \r\n\t').replace('Type', ''),
					'content': method_content.translate(None, ' \r\n\t')
				})
				self.secure_seek(to_big_close, 0)
			else:
				self.secure_read(to_big_open)
				logging.warning("unexpected jump")
				self.jump_to_close('{', '}')
				if not self.secure_read(1):
					break
				self.secure_seek(-1, 1)
		return methods_content

if __name__ == '__main__':
	p = Parser(TESTFILE1)
	
	#for key, val in p.find_methods().iteritems():
	for item in p.find_methods():
		print item['name']
