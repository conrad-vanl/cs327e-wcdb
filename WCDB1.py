import xml.etree.ElementTree as ET

class WCDB1:

  class XML:

    def __init__(self, element):
      self.tree = element

    @staticmethod
    def from_file(filename):
      """This function creates an Element object from an input file"""
      return WCDB1.XML( ET.parse( open(filename) ).getroot() )

    @staticmethod
    def from_string(string):
      """This function creates an Elemenct object from an input string"""
      return WCDB1.XML( ET.fromstring(string) )

    def __str__(self):
      return ET.tostring( self.tree )

    def export(self, filename):
      """This function converts an Element object into an xml file"""
      f = open(filename, 'w')
      f.write(self.__str__())
