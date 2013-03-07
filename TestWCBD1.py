# -------
# imports
# -------

import xml.etree.ElementTree
import StringIO
import io
import unittest
import os
import tempfile
from WCDB1 import *

class TestXML (unittest.TestCase):
	
	def test_from_file(self):
		#sub = tempfile.mkdtemp("sub")
		#sub.join("testfile.xml")
		#open("sub/testfile.xml").write("<note> \n<to>Tove</to>\n<from>Jani</from>\n<heading>Reminder</heading>\n<body>Don't forget me this weekend!</body>\n</note>\n")
		temp = tempfile.NamedTemporaryFile()
		temp.write('hello')
		temp.seek(0)
		file1 = WCDB1.XML.from_file("note.xml")
		file1.export("from_file.txt")
		self.assertTrue(open("note.xml").readlines() == open("from_file.txt").readlines())


	def test_from_file1(self):
		file2 = WCDB1.XML.from_file("note.xml")
		self.assertTrue(isinstance(file2, WCDB1.XML))

	def test_from_file2(self):
		file1 = WCDB1.XML.from_file("note.xml")
		file1.export("testwcbd1.txt")
		self.assertTrue(open("note.xml").readlines() == open("testwcbd1.txt").readlines())
	
	def test_from_string(self):
		seed_query = "<team> <abby> </abby> </team>"
		stringFile = WCDB1.XML.from_string(seed_query)
		self.assertTrue(stringFile.__str__() == seed_query)
	
	def test_from_string1(self):
		seed_query = '<organizations> <organization>World Health Organization </organization> </organizations>'
		stringFile = WCDB1.XML.from_string(seed_query)
		self.assertTrue(stringFile.__str__() == seed_query)
	
	def test_from_string2(self):
		seed_query = "<team> <abby> </abby> </team>"
		stringFile1 = WCDB1.XML.from_string(seed_query)
		self.assertTrue(isinstance(stringFile1, WCDB1.XML))

	def test_export(self):
		seed_query = "<team> <abby> </abby> </team>"
		exp1 = WCDB1.XML.from_string(seed_query)
		exp1.export("testwcbd1.txt")
		self.assertTrue(os.path.isfile('testwcbd1.txt'))

	def test_export1(self):
		seed_query = "<team> <abby> </abby> </team>"
		exp1 = WCDB1.XML.from_string(seed_query)
		exp1.export("testwcbd1.txt")
		self.assertTrue(open("testwcbd1.txt").readlines()[0] == seed_query)


	def test_export2(self):
		seed_query1 = "<organizations> <organization> World Health Organization </organization> </organizations>"
		exp3 = WCDB1.XML.from_string(seed_query1)
		exp3.export("testwcdb2.txt")
		self.assertTrue(os.path.isfile('testwcdb2.txt'))

print ("TestXML.py")
unittest.main()
print ("Done.")


