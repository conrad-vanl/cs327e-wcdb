# -------
# imports
# -------

import xml.etree.ElementTree
import StringIO
import io
import unittest
import os
import tempfile
from WCDB2 import *

class TestXML (unittest.TestCase):
	def test_from_file(self):
		temp = tempfile.NamedTemporaryFile()
		temp.write("<note> \n<to>Tove</to>\n<from>Jani</from>\n<heading>Reminder</heading>\n<body>Don't forget me this weekend!</body>\n</note>\n")
		temp.seek(0)
		file1 = XML.from_file(temp.name)
		file1.export("from_file.txt")
		self.assertTrue(open(temp.name).readlines()[0] == open("from_file.txt").readlines()[0])

print ("TestXML.py")
unittest.main()
print ("Done.")