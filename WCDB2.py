import xml.etree.ElementTree as ET
import os.path
import _mysql

# "Global" vars
MYSQL_CONNECT = { 
  "host"   : "cs327ewcdb.cz0aokgawzgn.us-east-1.rds.amazonaws.com", #"z",
  "user"   : "cs327ewcdb", #"<username>",
  "passwd" : "grouppassword", #"<password>",
  "db"     : "cs327ewcdb" #"downing_test"
}

# WCDB Wrapper class
class WCDB:

  class Factory:
    """General I/O Factory. This is where all the magic will happen eventually"""

    def __init__(self):
      # nothing for now
      return None

  class XML:
    """XML i/o utility"""

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


  class MySQL:
    """MySQL i/o utility and tools"""

    @staticmethod
    def login(**connection):
      """Logs in to MySQL Database and returns a MySQL connection"""

      # assert that the connection hash has all required elements
      assert( all(key in connection for key in ("host", "user", "passwd", "db")) )
        
      _c = _mysql.connect(**connection)
      #assert isinstance(_c, _mysql.connect)

      #self._c = _c
      return _c
