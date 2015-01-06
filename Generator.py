# coding: utf-8
import re

class Generator:
	filename = None
	methodinfos = []

	def __init__(self, filename, methodinfos):
		self.filename = filename
		self.methodinfos = methodinfos
	
	def __del__(self):
		pass
	
	def generate(self):
		print self.filename
		classname = self.filename.replace(".java", "")
		print "public class %sTest{" % classname
		print "\t%s target = new %s()" % (classname, classname)

		for methodinfo in self.methodinfos:
			methodname = re.sub(r'\W.*', "", methodinfo)
			print "\tpublic static void %sTest(){" % methodname
			print "\t\ttarget.%s" % methodinfo
			print "\t}"

		print "}"

if __name__ == '__main__':
	#g = Generator()
	pass
