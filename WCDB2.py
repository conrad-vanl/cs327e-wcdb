import xml.etree.ElementTree as ET
import os.path
import _mysql
"""Really wish I could split ths all up into multiple files/modules...."""


# ********************************************** 
# "GLOBAL" vars                              
# **********************************************

# Default Database Connection 
MYSQL_CONNECT = { 
  "host"   : "cs327ewcdb.cz0aokgawzgn.us-east-1.rds.amazonaws.com", #"z",
  "user"   : "cs327ewcdb", #"<username>",
  "passwd" : "grouppassword", #"<password>",
  "db"     : "cs327ewcdb" #"downing_test"
}

# Database Schemas
SCHEMAS = {
  "Crises":
    """
    crisis_id       VARCHAR(30) NOT NULL,
    crisisKind_id   VARCHAR(30) NOT NULL,
    name            TEXT NOT NULL,
    startDateTime   DATETIME NOT NULL,
    endDateTime     DATETIME,
    economicImpact   TEXT
    """,
  "RelatedPeople":
    """
    person_id       VARCHAR(30) NOT NULL,
    crisis_id       VARCHAR(30),
    organization_id VARCHAR(30)
    """,
  "RelatedOrganizations":
    """
    organization_id VARCHAR(30) NOT NULL,
    person_id       VARCHAR(30),
    crisis_id       VARCHAR(30)
    """,
  "RelatedCrises":
    """
    crisis_id       VARCHAR(30) NOT NULL,
    organization_id VARCHAR(30),
    person_id       VARCHAR(30)
    """,
  "Locations":
    """
    crisis_id       VARCHAR(30),
    organization_id VARCHAR(30),
    person_id       VARCHAR(30),
    locality        TEXT,
    region          TEXT,
    country         TEXT
    """,
  "ExternalResources":
    """
    crisis_id       VARCHAR(30),
    organization_id VARCHAR(30),
    person_id       VARCHAR(30),
    type            ENUM("ImageURL","VideoURL","MapURL","SocialNetworkURL","Citation","ExternalLinkUrl") NOT NULL,
    content         TEXT
    """,
  "HumanImpacts":
    """
    crisis_id       VARCHAR(30) NOT NULL,
    type            TINYTEXT,
    number          INT
    """,
  "ResourcesNeeded":
    """
    crisis_id       VARCHAR(30) NOT NULL,
    resource        TEXT
    """,
  "WaysToHelp":
    """
    crisis_id       VARCHAR(30) NOT NULL,
    waysToHelp      TEXT
    """,
  "Organizations":
    """
    organization_id                       VARCHAR(30) NOT NULL,
    organizationKind_id                   VARCHAR(30) NOT NULL,
    name                                  TEXT NOT NULL,
    history                               TEXT,
    telephone                  TEXT,
    fax                        TEXT,
    email                      TEXT,
    streetAddress              TEXT,
    locality            TEXT,
    region              TEXT,
    postalCode          TEXT,
    country             TEXT
    """,
  "OrganizationKinds":
    """
    organizationKind_id VARCHAR(30) NOT NULL,
    name                TEXT,
    description         TEXT
    """,
  "CrisisKinds":
    """
    crisisKind_id       VARCHAR(30) NOT NULL,
    name                TEXT,
    description         TEXT
    """,
  "PersonKinds":
    """
    personKind_id       VARCHAR(30) NOT NULL,
    name                TEXT,
    description         TEXT
    """,
  "People":
    """
    person_id           VARCHAR(30) NOT NULL,
    firstName           TEXT NOT NULL,
    lastName            TEXT NOT NULL,
    middleName          TEXT,
    suffix              TEXT,
    personKind_id       VARCHAR(30) NOT NULL
    """
}

DEFAULT_CONNECTION = None
DEFAULT_MAPPINGS   = None

# Setup defaults needed at runtimes
def main():
  global DEFAULT_CONNECTION
  DEFAULT_CONNECTION = MySQL()

  # Default mappings:
  # a mapping is a collection of tuples that map:
  #   xml_path, mapping, serializer function
  # where:
  #   xml_path is the serach path on the elementTree
  #   mapping is the argument for the serializer function
  #   serializer function is the ... serializer function!
  # 
  # a serializer function will location the element, map it out properly, and set its data on the model
  global DEFAULT_MAPPINGS
  DEFAULT_MAPPINGS = {
    "Person": [
      ("Person", ("personIdent", "person_id"), Serializers.Attribute ),
      ("Name/FirstName", "firstName", Serializers.Text),
      ("Name/LastName", "lastName", Serializers.Text),
      ("Name/MiddleName", "middleName", Serializers.Text),
      ("Name/Suffix", "suffix", Serializers.Text),
      ("Location", Location, Serializers.HasMany),
      ("ExternalResources", ExternalResources, Serializers.HasMany),
      ("Kind", ("personKindIdent", "personkind_id"), Serializers.Attribute)
    ],
    "Organization": [
      ("Organization", ("organizationIdent", "organization_id"), Serializers.Attribute ),
      ("Name", "name", Serializers.Text),
      ("ContactInfo/Telephone", "telephone", Serializers.Text),
      ("ContactInfo/Fax", "fax", Serializers.Text),
      ("ContactInfo/Email", "email", Serializers.Text),
      ("ContactInfo/PostalAddress/StreetAddress", "streetAddress", Serializers.Text),
      ("ContactInfo/PostalAddress/Locality", "locality", Serializers.Text),
      ("ContactInfo/PostalAddress/Region", "region", Serializers.Text),
      ("ContactInfo/PostalAddress/PostalCode", "postalCode", Serializers.Text),
      ("ContactInfo/PostalAddress/Country", "country", Serializers.Text)
    ],
    "Location": [
      ("Locality", "locality", Serializers.Text),
      ("Region", "region", Serializers.Text),
      ("Country", "country", Serializers.Text)
    ],
    "ExternalResources": [
      ("ImageURL", "type", Serializers.Text),
      ("VideoURL", "type", Serializers.Text),
      ("MapURL", "type", Serializers.Text),
      ("SocialNetworkURL", "type", Serializers.Text),
      ("ExternalLinkURL", "type", Serializers.Text),
      ("Citation", "type", Serializers.Text)
      ],
    "Crisis": [
      ("Crisis", ("crisisIdent", "crisis_id"), Serializers.Attribute),
      ("Name", "name", Serializers.Text),
      ("Kind", ("crisisKindIdent", "crisiskind_id"), Serializers.Attribute),
      ("Location", Location, Serializers.HasMany),
      ("StartDateTime/Date", "startDateTime", Serializers.Text),
      ("EndDateTime/Date", "endDateTime", Serializers.Text),
      ("HumanImpact/Type", "type", Serializers.Text),
      ("HumanImpact/Number", "number", Serializers.Text),
      ("EconomicImpact", "economicImpact", Serializers.Text),
      ("ResourceNeeded", ResourcesNeeded, Serializers.HasMany),
      ("WaysToHelp", WaysToHelp, Serializers.HasMany),
      ("RelatedPersons", RelatedPeople, Serializers.HasMany),
      ("RelatedOrganizations", RelatedOrganizations, Serializers.HasMany)
    ],
    "ResourcesNeeded": [
      ("ResouceNeeded", "resource", Serializers.Text)
    ],
    "WaysToHelp": [
      ("WaysToHelp", "waysToHelp", Serializers.Text)
    ]
  }




# ********************************************** 
#                 FACTORY Class                                  
# ----------------------------------------------              
# - creates Models (and persist to DB) from XML
# - creates XML from Models
# ----------------------------------------------
# Usage:
#   Initialize empty database and prepare for i/o
#     factory = WCDB2.Factory()
#
#   Import XML 
#
#   Export XML
#
# ********************************************** 
class Factory:
  """General I/O Factory. This is what ties everything together - it initializes the database, imports XML into the database, exports XML from the database, etc."""

  def __init__(self, **options):
    """Initializes everything!"""
    # Setup MySQL connection
    self._c = MySQL()
    DEFAULT_CONNECTION = self._c

    # Setup tables
    self._c.setup_database()

  def import_xml(self, xml):
    """Imports XML (must be initialized already) into database"""

    # Basic idea: loop over root elements in XML and apply some sort of mapping function, then save the result:
    for element in xml.tree:
      self.lookup_model(element.tag).from_xml(element).persist()

  def export_xml(self, filename):
    """Exports XML from database"""

  def lookup_model(self, model_name):
    """Lookup model class from model_name, returns Class"""
    return eval(model_name) # just do this until we have problems





# ********************************************** 
#                 XML Class                                  
# ----------------------------------------------              
# - parses/loads XML documents
# - create/exports XML documents
# ----------------------------------------------
# Usage:
#   Initialize XML from etree.element:
#     xml = WCDB2.XML(element)  # element must be a etree.element
#
#   Initialize XML from XML file:
#     xml = WCDB2.XML.from_file(filename)
#
#   Initialize XML from XML string:
#     xml = WCDB2.XML.from_string(xml_string)
#
#   Get XML string:
#     str(xml)
#
#   Export XML to a file:
#     xml.export(filename)
# ********************************************** 
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







# ********************************************** 
#                 MySQL Class                                  
# ----------------------------------------------              
# - initializes database connection
# - sets up database tables
# - perform RAW SQL queries on database
# ----------------------------------------------
# Usage:
#   Initialize new database connection:
#     mysql = WCDB2.MySQL(connection_params)
#
#   Run SQL query on database:
#     mysql.query("show tables")
#
#   Setup tables based on loaded schema
#   (drops tables, creates new tables)
#     mysql.setup_database()
#
# ********************************************** 
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








# ********************************************** 
#                   MODEL                                
# ----------------------------------------------              
#
# ----------------------------------------------
#
# ********************************************** 
# Internal: I'm hoping that splitting out each relation into it's own model/class will pay off in the long run
# Each model should have from_xml, to_xml methods
# Each model should have a plural, table_name attributes
class Model:
  """
    A model is a mapper/representation of a relation. allows us to split up tasks a little easier.
    Basically, a model will be responsible for:
      - the serialization to/from xml of itself
      - persisting itself to the DB
  """  
  table_name = ""
  plural = ""
  hasMany = [] # [Model]
  belongsTo = [] # [Model]
  keys = []
  foreign_key = ""

  def __init__(self, **params):
    """Initializes a new model with the given params"""
    self.params = {}
    for key, value in params.items():
      self.set(key, value)

  def get(self, key):
    """Get an attribute/associative model"""
    return self.params.get(key)

  def set(self, key, value):
    """Set an attribute/associative model"""
    return self.params.__setitem__(key, value)

  @classmethod
  def from_xml(_class, xml, mappings = None):
    """Creates model from xml"""
    # initialize empty model
    model = _class()

    # conform xml to proper type
    if isinstance(xml, basestring):
      xml = XML.from_string(xml)

    # revert to default mappings if not supplied
    if mappings == None:
      mappings = DEFAULT_MAPPINGS[_class.__name__]

    # loop through mappings
    for _map in mappings:
      # _map is a tuple
      # first element is XML +path+
      # second element is either:
      #   string: key                       => key = xml_element.find(path).text()
      #   modelClass: HAS_MANY association  => key = modelClass.plural() = **create each from_xml and return array: xml_element.findAll(path)**
      #   tuple: (attribute, key)           => key = xml_element.find(path).get(attribute)
      # third element is the serialization function to be used
      _map[2].from_xml(model, xml, _map[0], _map[1])     

    return model

  def to_xml(self):
    """returns xml string of model"""
    raise Exception("Must override method")

  @classmethod
  def all(cls, connection = None):
    """Quick hack just to be able to experiment, returns all records in table"""

    if connection == None:
      connection = DEFAULT_CONNECTION

    a = connection.query("select * from " + cls.table_name, how = 1)
    return a

  def persist(self, connection = None):
    """Persists model to DB, including all associations (TODO)"""

    if connection == None:
      connection = DEFAULT_CONNECTION

    # Persist model to DB:
    return connection.query("insert into `"+str(self.table_name)+"` ("+",".join(self.keys)+") values("+",".join('"{0}"'.format(w) for w in self.vals())+")")

  def vals(self):
    """returns a list [in order of keys] of attribute values"""
    result = []
    for key in self.keys:
      result.append(self.get(key))
    return result



# ********************************************** 
#                  SERIALIZERS                                  
# ----------------------------------------------              
#
# ----------------------------------------------
#
# ********************************************** 
class Serializers():
  """Serialization class to take models from one data type to another"""

  class Text():
    """Simple serializer that retrieves text value on element, such as <element>text value</element>"""
    @staticmethod
    def from_xml(model, xml_element, path, key):
      element = xml_element.find(path)
      if element is not None:
        model.set(key, element.text)

  class HasMany():
    """Serializer that initializes elements from a hasMany association"""
    @staticmethod
    def from_xml(model, xml_element, path, foreignModel):
      elements = xml_element.findall(path)
      if elements is not None:
        # create foreign objects
        foreign_records = []
        for e in elements:
          foreign_records.append(foreignModel.from_xml(e))
        # set relation on model
        model.set(foreignModel.plural, foreign_records)

  class Attribute():
    """Simple serialize that retrieves attribute value on element, such as <element attr="val" />"""
    @staticmethod
    def from_xml(model, xml_element, path, (attribute, key)):
      # first check if looking for root element:
      if path == model.__class__.__name__:
        element = xml_element
      else:
        element = xml_element.find(path)

      if element is not None:
        model.set(key, element.attrib.get(attribute))







# ********************************************** 
#               INDIVIDUAL MODELS                                 
# ----------------------------------------------              
#
# ----------------------------------------------
#
# ********************************************** 
# NOW for the actual models:
class Crisis(Model):
  plural = "crises"
  table_name = "Crises"
  foreign_key = "crisis_id"
  keys = ["crisis_id", "crisisKind_id", "name", "startDateTime", "endDateTime", "economicImpact"]

class RelatedPerson(Model):
  plural = "relatedPeople"
  table_name = "RelatedPeople"
  keys = ["person_id","crisis_id","organization_id"]

class RelatedOrganization(Model):
  plural = "relatedOrganizations"
  table_name = "RelatedOrganizations"
  keys = ["person_id","crisis_id","organization_id"]

class RelatedCrisis(Model):
  plural = "relatedCrises"
  table_name = "RelatedCrises"
  keys = ["person_id","crisis_id","organization_id"]

class Location(Model):
  plural = "locations"
  table_name = "Locations"
  keys = ["crisis_id","person_id","organization_id","locality","region","country"]

class ExternalResource(Model):
  plural = "externalResources"
  table_name= "ExternalResources"
  keys = ["crisis_id","organization_id","type","content"]

class HumanImpact(Model):
  plural = "humanImpacts"
  table_name = "HumanImpact"
  keys = ["crisis_id","resource","type"]

class ResourceNeeded(Model):
  plural = "resourcesNeeded"
  table_name = "ResourcesNeeded"
  keys = ["crisis_id", "resource"]

class WayToHelp(Model):
  pural = "waysToHelp"
  table_name = "WaysToHelp"
  foreign_key = "wayToHelp_id"
  keys = ["crisis_id","waysToHelp"]

class Organization(Model):
  plural = "organizations"
  table_name = "Organizations"
  foreign_key = "organization_id"
  keys = ["organization_id","organizationKind_id","name","history","telephone","fax","email","streetAddress","locality","region","postalCode","country"]

class OrganizationKind(Model):
  plural = "organizationKinds"
  table_name = "OrganizationKinds"
  foreign_key = "organizationKind_id"
  keys = ["organizationKind_id","name","description"]

class CrisisKind(Model):
  plural = "crisisKinds"
  table_name = "CrisisKinds"
  foreign_key = "crisisKind_id"
  keys = ["crisisKind_id","name","description"]

class PersonKind(Model):
  plural = "personKinds"
  table_name = "PersonKinds"
  foreign_key = "personKind_id"
  keys = ["personKind_id","name","description"]

class Person(Model):
  plural = "people"
  table_name = "People"
  foreign_key = "person_id"
  keys = ["person_id","firstName","lastName","middleName","suffix","personKind_id"]

# call up runetime stuff:
main()
