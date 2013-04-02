import xml.etree.ElementTree as ET
import os.path

# "Global" vars
MYSQL_CONNECT = 
{ 
  host   : "external-db.s6813.gridserver.com", #"z",
  user   : "db6813_cs327e", #"<username>",
  passwd : "grouppassword", #"<password>",
  db     : "db6813_cs327e" #"downing_test"
}

# WCDB Wrapper class
class WCDB:

  """General I/O Factory. This is where all the magic happens"""
  class Factory:
    def __init__(self):
      # nothing for now

  """XML i/o utility"""
  class XML:

    def __init__(self, element):
      """Creates an WCDB:XML object. Argument must be an xml.etree.Element!"""

      assert isinstance(element, ET.Element)
      self.tree = element

    @staticmethod
    def from_file(filename):
      """Creates an WCDB:XML object from an input file"""

      assert os.path.isfile(filename)
      return WCDB.XML( ET.parse( open(filename) ).getroot() )

    @staticmethod
    def from_string(string):
      """Creates an WCDB:XML object from an input string"""

      assert isinstance(string, str) or isinstance(string, basestring)
      return WCDB.XML( ET.fromstring(string) )

    def __str__(self):
      return ET.tostring( self.tree )

    def export(self, filename):
      """Converts an WCDB:XML object into an xml file"""
      f = open(filename, 'w')
      f.write(self.__str__())


  """MySQL i/o utility and tools"""
  class MySQL: