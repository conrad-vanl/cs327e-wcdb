# -------
# imports
# -------

import xml.etree.ElementTree
import StringIO
import io
import unittest
import os
import tempfile
import WCDB2  
import types
import xml.etree.ElementTree as ET

class TestWCDB2 (unittest.TestCase):
	def test_from_file(self):
		temp = tempfile.NamedTemporaryFile()
		temp.write("<note> \n<to>Tove</to>\n<from>Jani</from>\n<heading>Reminder</heading>\n<body>Don't forget me this weekend!</body>\n</note>\n")
		temp.seek(0)
		file1 = WCDB2.XML.from_file(temp.name)
		file1.export("from_file.txt")
		self.assertTrue(open(temp.name).readlines()[0] == open("from_file.txt").readlines()[1])

	def test_from_file1(self):
		temp = tempfile.NamedTemporaryFile()
		temp.write("<note> \n<to>Tove</to>\n<from>Jani</from>\n<heading>Reminder</heading>\n<body>Don't forget me this weekend!</body>\n</note>\n")
		temp.seek(0)
		file2 = WCDB2.XML.from_file(temp.name)
		self.assertTrue(isinstance(file2, WCDB2.XML))

	def test_from_file2(self):
		temp = tempfile.NamedTemporaryFile()
		temp.write("<team> <abby> </abby> </team>")
		temp.seek(0)
		file3 = WCDB2.XML.from_file(temp.name)
		file3.export(temp.name)
		self.assertTrue(open(temp.name).readlines() == open("wcdb1.txt").readlines())

	def test_from_string(self):
		seed_query = "<team> <abby> </abby> </team>"
		stringFile = WCDB2.XML.from_string(seed_query)
		self.assertTrue(stringFile.__str__() == seed_query)
	
	def test_from_string1(self):
		seed_query = '<organizations> <organization>World Health Organization </organization> </organizations>'
		stringFile = WCDB2.XML.from_string(seed_query)
		self.assertTrue(stringFile.__str__() == seed_query)
	
	def test_from_string2(self):
		seed_query = "<team> <abby> </abby> </team>"
		stringFile1 = WCDB2.XML.from_string(seed_query)
		self.assertTrue(isinstance(stringFile1, WCDB2.XML))

	def test_export(self):
		seed_query = "<team> <abby> </abby> </team>"
		exp1 = WCDB2.XML.from_string(seed_query)
		exp1.export("wcdb1.txt")
		self.assertTrue(os.path.isfile('wcdb1.txt'))

	def test_export1(self):
		seed_query = "<team> <abby> </abby> </team>"
		exp1 = WCDB2.XML.from_string(seed_query)
		exp1.export("testwcbd1.txt")
		self.assertTrue(open("testwcbd1.txt").readlines()[1] == seed_query)

	def test_export2(self):
		seed_query1 = "<organizations> <organization> World Health Organization </organization> </organizations>"
		exp3 = WCDB2.XML.from_string(seed_query1)
		exp3.export("wcdb2.txt")
		self.assertTrue(os.path.isfile('wcdb2.txt'))

	def test_login(self):
		testDict = WCDB2.MYSQL_CONNECT
		testConnect = WCDB2.MySQL.login(**testDict)
		self.assertTrue(type (testDict) == types.DictType)

	def test_login2(self):
		testDict = WCDB2.MYSQL_CONNECT
		testConnect = WCDB2.MySQL.login(**testDict)
		self.assertTrue(str(type(testConnect)) == "<type '_mysql.connection'>")

	def test_login3(self):
		testConnect = WCDB2.MySQL.login(**WCDB2.MYSQL_CONNECT)
		self.assertTrue('open' in str(testConnect))		

	def test_query(self):
		testQuery = WCDB2.DEFAULT_CONNECTION.query("show databases")
		self.assertTrue(type(testQuery) == types.TupleType)


	def test_query1(self):
		testQuery = WCDB2.DEFAULT_CONNECTION.query("show databases")
		testQuery1 = WCDB2.DEFAULT_CONNECTION.query("use "+testQuery[1]['Database'])
		self.assertTrue(type(testQuery1) == types.NoneType)		

	def test_query2(self):
		testQuery = WCDB2.DEFAULT_CONNECTION.query("show databases")
		testQuery1 = WCDB2.DEFAULT_CONNECTION.query("use "+testQuery[2]['Database'])
		self.assertTrue(type(testQuery1) == types.NoneType)	

	def test_setup_database(self):
		testSetup = WCDB2.DEFAULT_CONNECTION.setup_database()
		self.assertTrue(type(testSetup) == types.NoneType)	

	def test_setup_database1(self):
		testSetup = WCDB2.DEFAULT_CONNECTION.setup_database()
		testQuery = WCDB2.DEFAULT_CONNECTION.query("show databases")
		self.assertTrue(type(testQuery) == types.TupleType)
		
	def test_setup_database1(self):
		testSetup = WCDB2.DEFAULT_CONNECTION.setup_database()	
		testQuery = WCDB2.DEFAULT_CONNECTION.query("show databases")
		self.assertTrue(len(testQuery)!= 0 )

	def test_drop_table(self):
		testQuery = WCDB2.DEFAULT_CONNECTION.query("show databases")
		testQuery1 = WCDB2.DEFAULT_CONNECTION.drop_table('nsd')
		self.assertTrue(type(testQuery1)==types.NoneType)


	def test_get(self):
		sampleDict = {'a' : '1'}
		testGet = WCDB2.Model(**sampleDict)
		test1 = WCDB2.Model.get(testGet, 'a')
		self.assertTrue(test1 == '1')

	def test_get2(self):
		sampleDict = {'a' : 'b'}
		testGet = WCDB2.Model(**sampleDict)
		test1 = WCDB2.Model.get(testGet, 'a')
		self.assertTrue(test1 == 'b')

	def test_get3(self):
		sampleDict = {'b' : '3', 'r': '55', 'te':'323'}
		testGet = WCDB2.Model(**sampleDict)
		test1 = WCDB2.Model.get(testGet, 'b')
		self.assertTrue(test1 == '3')		

	def test_set(self):
		sampleDict = {'a' : '1'}
		testSet = WCDB2.Model(**sampleDict)
		WCDB2.Model.set(testSet, 'a', '2')
		test2 = WCDB2.Model.get(testSet, 'a')
		self.assertTrue(test2 == '2')

	def test_set2(self):
		sampleDict = {'a' : 'b'}
		testSet = WCDB2.Model(**sampleDict)
		WCDB2.Model.set(testSet, 'a', 'c')
		test2 = WCDB2.Model.get(testSet, 'a')
		self.assertTrue(test2 == 'c')
	
	def test_set3(self):
		sampleDict = {'b' : '3', 'r': '55', 'te':'323'}
		testSet = WCDB2.Model(**sampleDict)
		WCDB2.Model.set(testSet, 'r', '2')
		test2 = WCDB2.Model.get(testSet, 'r')
		self.assertTrue(test2 == '2')

	def test_lookup_model(self):
		y = WCDB2.lookup_model('1+1')
		self.assertTrue(y==2)

	def test_lookup_model2(self):
		lookupTest = WCDB2.lookup_model('1+1')
		lookupTest1 = eval('1+1')
		self.assertTrue(lookupTest1==lookupTest)

	def test_lookup_model3(self):
		lookupTest = WCDB2.lookup_model('1+1')
		self.assertTrue(type(lookupTest) == types.IntType)

	def test_lookup_model_from_plural(self):
		test = WCDB2.lookup_model_from_plural('crises')
		self.assertTrue( WCDB2.Crisis == test)

	def test_lookup_model_from_plural2(self):
		test = WCDB2.lookup_model_from_plural(WCDB2.Person.plural)
		self.assertTrue( WCDB2.Person == test)

	def test_lookup_model_from_plural3(self):
		test = WCDB2.lookup_model_from_plural('ASD')
		self.assertTrue(type(test)== types.NoneType)

	def test_import_xml(self):
		file2 = WCDB2.XML.from_file('RunWCDB2a.in.xml')
		file1 = open('RunWCDB2a.in.xml')
		testString = ''
		for i in file1:
			testString+=i
		test_factory = WCDB2.Factory()
		stringFile = WCDB2.XML.from_string(testString)
		test_factory.import_xml(stringFile)
		#WCDB2.Factory.import_xml(seed_query)



print ("TestXML.py")
unittest.main()
print ("Done.")