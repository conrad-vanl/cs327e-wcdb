import xml.etree.ElementTree as ET
import os.path

class WCDB:

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
