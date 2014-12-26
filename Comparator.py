#coding: utf-8
from Parser import Parser

class Comparator:
	p1 = None
	p2 = None
	methods1 = None
	methods2 = None
	same_method = None

	def __init__(self, orig, dev):
		self.p1 = Parser(orig)
		self.p2 = Parser(dev)
		self.methods1 = []
		self.methods2 = []
		self.same_method = []
	
	def __del__(self):
		pass
	
	def compare(self):
		self.methods1 = self.p1.find_methods()
		self.methods2 = self.p2.find_methods()
	
	def dump_method_name(self):
		print "print original methods name below"
		for method in self.methods1:
			print "\t" + method['name']

		print "print develop methods name below"
		for method in self.methods1:
			print "\t" + method['name']
	
	def dump_method_content(self):
		print "print original methods content below"
		for method in self.methods1:
			print "\t" + method['content']

		print "print develop methods content below"
		for method in self.methods1:
			print "\t" + method['content']
	
	def pick_same_method_name(self):
		self.same_method = []
		for orig_method in self.methods1:
			dev_same_method = [item for item in self.methods2 if item['name'] == orig_method['name']]
			if 0 < len(dev_same_method):
				self.same_method.append(orig_method['name'])
		return self.same_method
	
if __name__ == '__main__':
	c = Comparator(DIR1, DIR1)
	c.compare()
	c.dump_method_name()
