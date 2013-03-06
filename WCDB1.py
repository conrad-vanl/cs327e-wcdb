import xml.etree.ElementTree as ET

class WCDB1:

  class XML:

    def __init__(self, etree):
      self.tree = etree

    @staticmethod
    def from_file(filename):
      return WCDB1.XML( ET.parse( open(filename) ) )

    @staticmethod
    def from_string(string):
      return WCDB1.XML( ET.fromstring(string) )

    def __str__(self):
      return ET.tostring( self.tree.getroot() )

    def export(self, filename):
      f = open(filename, 'w')
      f.write(self.__str__())