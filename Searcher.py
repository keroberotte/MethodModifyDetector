# coding: utf-8
import CONSTS
import fnmatch
import os
import logging

class Searcher:
	root = None

	def __init__(self, root):
		self.root = root
	
	def __del__(self):
		pass
	
	def search(self):
		files = []
		for root, dirnames, filenames in os.walk(self.root):
			for filename in fnmatch.filter(filenames, "*.java"):
				files.append({
					'dir': root,
					'filename': filename
				})
		return files

if __name__ == '__main__':
	s = Searcher(CONSTS.O_DIR1)
	for file_info in s.search():
		print file_info
