import xml.etree.ElementTree as ET
import os.path
import _mysql
"""Really wish I could split ths up into multiple files...."""


# "Global" vars
MYSQL_CONNECT = { 
  "host"   : "cs327ewcdb.cz0aokgawzgn.us-east-1.rds.amazonaws.com", #"z",
  "user"   : "cs327ewcdb", #"<username>",
  "passwd" : "grouppassword", #"<password>",
  "db"     : "cs327ewcdb" #"downing_test"
}

SCHEMAS = {
  "Crises":
    """
    crisis_id       VARCHAR(30) NOT NULL,
    crisisKind_id   VARCHAR(30) NOT NULL,
    name            TEXT NOT NULL,
    startDateTime   DATETIME NOT NULL,
    endDateTime     DATETIME,
    ecnomicImpact   TEXT
    """ 
}
#, "RelatedPeople", "RelatedOrganizations", "RelatedCrises", "Locations", "ExternalResources", "HumanImpacts", "ResourcesNeeded", "WaysToHelp", "Organizations", "OrganizationKinds", "CrisisKinds", "PersonKinds", "People"}

DEFAULT_CONNECTION = MySQL()

class Factory:
  """General I/O Factory. This is what ties everything together - it initializes the database, imports XML into the database, exports XML from the database, etc."""

  def __init__(self, **options):
    """Initializes everything!"""
    # Setup MySQL connection
    self._c = MySQL()
    DEFAULT_CONNECTION = self._c

    # Setup tables
    self._c.setup_database()
    
  def import_xml_from_file(self, xml):
    """Import XML file into database"""

  def import_xml_from_string(self, string):
    """Import XML STRING into database"""

  def export_xml(self):
    """Exports XML from database"""


class XML:
  """XML I/O utility and tools"""

  def __init__(self, element):
    """Creates an XML object. Argument must be an xml.etree.Element!"""

    assert isinstance(element, ET.Element)
    self.tree = element

  @staticmethod
  def from_file(filename):
    """Creates an XML object from an input file"""

    assert os.path.isfile(filename)
    return XML( ET.parse( open(filename) ).getroot() )

  @staticmethod
  def from_string(string):
    """Creates an XML object from an input string"""

    assert isinstance(string, str) or isinstance(string, basestring)
    return XML( ET.fromstring(string) )

  def __str__(self):
    return ET.tostring( self.tree )

  def export(self, filename):
    """Converts an XML object into an xml file"""
    f = open(filename, 'w')
    f.write(self.__str__())


class MySQL:
  """MySQL I/O utility and tools"""

  @staticmethod
  def login(**connection):
    """Logs in to MySQL Database and returns a MySQL connection"""

    # assert that the connection hash has all required elements
    assert( all(key in connection for key in ("host", "user", "passwd", "db")) )
      
    _c = _mysql.connect(**connection)
    return _c

  def __init__(self, c = MYSQL_CONNECT):
    """Creates MySQL object and sets up database"""
    # Create db connection
    self._c = MySQL.login(**c)

    # Setup db
    # self.setup_database()

  def query (self, query, **options) :
    """Runs MySQL query on database"""
    # Setup options:
    maxrows = options.get("maxrows", 0) # default to 0 / no max
    how     = options.get("how", 1) # default to table.column syntax

    assert str(type(self._c)) == "<type '_mysql.connection'>"
    assert type(query)      is str

    self._c.query(query)
    r = self._c.store_result()

    if r is None :
      return None

    assert str(type(r)) == "<type '_mysql.result'>"
    t = r.fetch_row(maxrows, how)
    assert type(t) is tuple
    return t

  def setup_database(self, schemas = SCHEMAS):
    """Sets up database"""
    assert str(type(self._c)) == "<type '_mysql.connection'>"

    # setup tables
    for table, schema in schemas.iteritems():
      # first, drop table
      self.drop_table(table)

      # now create table
      self.create_table(table, schema)

  def drop_table(self, table):
    """Drops a table (if it exists)"""
    return self.query("drop table if exists "+table+";")

  def create_table(self, table, schema):
    """Creates +table+ from +schema+"""
    return self.query("create table "+table+" ("+schema+")")


class Models:
  """A model is a mapper/representation of a relation. allows us to split up tasks a little easier.
    Basically, a model will be responsible for:
      - the serialization to/from xml of itself
      - persisting itself to the DB
  """
  # Internal: I'm hoping that splitting out each relation into it's own model/class will pay off in the long run
  # Each model should have from_xml, to_xml methods
  # Each model should have a plural, table_name attributes

  class Base:
    """This is the base model class that each relation will inherit"""
    table_name = ""
    plural = ""

    def __init__(self, **params):
      """Initializes a new model with the given params"""
      self.params = params

    def from_xml(self, xml_string):
      """Creates model from xml"""
      raise Exception("Must override method")

    def to_xml(self):
      """returns xml string of model"""
      raise Exception("Must override method")

    @classmethod
    def select(cls, filter_function = lambda v: True, connection = DEFAULT_CONNECTION):
      """Quick hack just to be able to experiment"""
      a = connection.query("select * from " + cls.table_name, how = 1)
      x = []
      for v in a:
        if(filter_function(v)):
          x.append(v)
      return x

    def persist(self, c = None):
      """Persists model to DB"""
      if c is None:
        c = DEFAULT_CONNECTION
      return c.query("insert into `"+str(self.table_name)+"` ("+",".join(self.params.keys())+") values("+",".join('"{0}"'.format(w) for w in self.params.values())+")")


# NOW for the actual models:
class Crisis(Models.Base):
  plural = "crises"
  table_name = "Crises"

