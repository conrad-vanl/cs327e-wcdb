# -------
# imports
# -------

import StringIO
import io
import unittest

from WCDB1 import *

class TestXML (unittest.TestCase):

	seed_data = "<thu><team><abby></abby><john></john><paul></paul></team><taketwo><team><abby></abby></team></taketwo><team></team></thu>"
  	seed_query = "<team><abby></abby></team>"
	
	def test_from_file(self):
		file1 = WCDB1.XML.from_file("note.xml")
		file1.export("testwcbd1.txt")
		self.assertTrue(open("note.xml").readlines() == open("testwcbd1.txt").readlines())

print ("TestXML.py")
unittest.main()
print ("Done.")


