#coding: utf-8
import CONSTS
from Comparator import Comparator
from Searcher import Searcher
from Generator import Generator

if __name__ == '__main__':
	s1 = Searcher(CONSTS.O_DIR1)
	s2 = Searcher(CONSTS.D_DIR1)
	
	orig_files = s1.search()
	dev_files = s2.search()
	
	for f1 in orig_files:
		f2 = [item for item in dev_files if item['filename'] == f1['filename']]
		if len(f2) <= 0:
			continue
		f2 = f2[0]
		c = Comparator(
			"%s/%s" % (f1['dir'], f1['filename']),
			"%s/%s" % (f2['dir'], f2['filename'])
		)
		c.compare()

		modified = c.get_modified_method()
		if len(modified) <= 0:
			continue
		#print f1['filename']
		#for methodinfo in modified:
		#	print "\t%s" % methodinfo
		g = Generator(f1['filename'], modified)
		g.generate()


	#c.dump_method_content()
	#c.pick_same_method_name()"""
