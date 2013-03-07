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
		temp = tempfile.NamedTemporaryFile()
		temp.write("<note> \n<to>Tove</to>\n<from>Jani</from>\n<heading>Reminder</heading>\n<body>Don't forget me this weekend!</body>\n</note>\n")
		temp.seek(0)
		file1 = WCDB1.XML.from_file(temp.name)
		file1.export("from_file.txt")
		self.assertTrue(open(temp.name).readlines()[0] == open("from_file.txt").readlines()[0])


	def test_from_file1(self):
		temp = tempfile.NamedTemporaryFile()
		temp.write("<note> \n<to>Tove</to>\n<from>Jani</from>\n<heading>Reminder</heading>\n<body>Don't forget me this weekend!</body>\n</note>\n")
		temp.seek(0)
		file2 = WCDB1.XML.from_file(temp.name)
		self.assertTrue(isinstance(file2, WCDB1.XML))

	def test_from_file2(self):
		temp = tempfile.NamedTemporaryFile()
		temp.write("<team> <abby> </abby> </team>")
		temp.seek(0)
		file3 = WCDB1.XML.from_file(temp.name)
		file3.export(temp.name)
		self.assertTrue(open(temp.name).readlines() == open("testwcbd1.txt").readlines())
	
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
		exp1.export("testwcdb1.txt")
		self.assertTrue(os.path.isfile('testwcdb1.txt'))

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


