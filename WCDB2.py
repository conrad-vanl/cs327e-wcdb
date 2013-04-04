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
    startDate       DATE,
    startTime       TIME,
    endDate         DATE,
    endTime         TIME,
    economicImpact  TEXT
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
MYSQL_DEBUG = False

# Setup defaults needed at runtimes
def main():
  global DEFAULT_CONNECTION
  DEFAULT_CONNECTION = MySQL()

  global XML_ROOT_ELEMENTS
  XML_ROOT_ELEMENTS = [Crisis, Organization, Person, CrisisKind, OrganizationKind, PersonKind]

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
      (".", ("personIdent", "person_id"), Serializers.Attribute),
      ("Name/FirstName", "firstName", Serializers.Text),
      ("Name/LastName", "lastName", Serializers.Text),
      ("Name/MiddleName", "middleName", Serializers.Text),
      ("Name/Suffix", "suffix", Serializers.Text),
      ("Location", Location, Serializers.HasMany),
      ("ExternalResources/*", ExternalResource, Serializers.HasMany),
      ("Kind", ("personKindIdent", "personKind_id"), Serializers.Attribute),
      ("RelatedPersons/*", RelatedPerson, Serializers.HasMany),
      ("RelatedOrganizations/*", RelatedOrganization, Serializers.HasMany)
    ],
    "RelatedPerson": [
      (".", ("personIdent", "person_id"), Serializers.Attribute)
    ],
    "RelatedOrganization": [
      (".", ("organizationIdent", "organization_id"), Serializers.Attribute)
    ],
    "RelatedCrisis": [
      (".", ("crisisIdent", "crisis_id"), Serializers.Attribute)
    ],
    "Organization": [
      (".", ("organizationIdent", "organization_id"), Serializers.Attribute ),
      ("Name", "name", Serializers.Text),
      ("History", "history", Serializers.Text),
      ("ContactInfo/Telephone", "telephone", Serializers.Text),
      ("ContactInfo/Fax", "fax", Serializers.Text),
      ("ContactInfo/Email", "email", Serializers.Text),
      ("ContactInfo/PostalAddress/StreetAddress", "streetAddress", Serializers.Text),
      ("ContactInfo/PostalAddress/Locality", "locality", Serializers.Text),
      ("ContactInfo/PostalAddress/Region", "region", Serializers.Text),
      ("ContactInfo/PostalAddress/PostalCode", "postalCode", Serializers.Text),
      ("ContactInfo/PostalAddress/Country", "country", Serializers.Text),
      ("Kind", ("organizationKindIdent", "organizationKind_id"), Serializers.Attribute),
      ("RelatedPersons/*", RelatedPerson, Serializers.HasMany),
      ("RelatedCrises/*", RelatedCrisis, Serializers.HasMany),
      ("ExternalResources/*", ExternalResource, Serializers.HasMany),
      ("Location", Location, Serializers.HasMany)
    ],
    "Location": [
      ("Locality", "locality", Serializers.Text),
      ("Region", "region", Serializers.Text),
      ("Country", "country", Serializers.Text)
    ],
    "ExternalResource": [
      (".", "type", Serializers.Tag),
      (".", "content", Serializers.Text)
    ],
    "HumanImpact": [
      ("Type", "type", Serializers.Text),
      ("Number", "number", Serializers.Text)
    ],
    "ResourceNeeded": [
      (".", "resource", Serializers.Text)
    ],
    "Crisis": [
      (".", ("crisisIdent", "crisis_id"), Serializers.Attribute),
      ("Name", "name", Serializers.Text),
      ("Kind", ("crisisKindIdent", "crisisKind_id"), Serializers.Attribute),
      ("Location", Location, Serializers.HasMany),
      ("StartDateTime/Date", "startDate", Serializers.Text),
      ("StartDateTime/Time", "startTime", Serializers.Text),
      ("EndDateTime/Date", "endDate", Serializers.Text),
      ("EndDateTime/Time", "endDate", Serializers.Text),
      ("HumanImpact", HumanImpact, Serializers.HasMany),
      ("EconomicImpact", "economicImpact", Serializers.Text),
      ("ResourceNeeded", ResourceNeeded, Serializers.HasMany),
      ("WaysToHelp", WaysToHelp, Serializers.HasMany),
      ("RelatedPersons/*", RelatedPerson, Serializers.HasMany),
      ("ExternalResources/*", ExternalResource, Serializers.HasMany),
      ("RelatedOrganizations/*", RelatedOrganization, Serializers.HasMany)
    ],
    "WaysToHelp": [
      (".", "waysToHelp", Serializers.Text)
    ],
    "OrganizationKind": [
      (".", ("organizationKindIdent", "organizationKind_id"), Serializers.Attribute),
      ("Name", "name", Serializers.Text),
      ("Description", "description", Serializers.Text)
    ],
    "PersonKind": [
      (".", ("personKindIdent", "personKind_id"), Serializers.Attribute),
      ("Name", "name", Serializers.Text),
      ("Description", "description", Serializers.Text)
    ],
    "CrisisKind": [
      (".", ("crisisKindIdent", "crisisKind_id"), Serializers.Attribute),
      ("Name", "name", Serializers.Text),
      ("Description", "description", Serializers.Text)
    ]
  }

def lookup_model(model_name):
  """Lookup model class from model_name, returns Class"""
  return eval(model_name) # just do this until we have problems

def lookup_model_from_plural(plural):
  """Lookup model class from a plural model_name, returns Class"""
  model_classes = Model.__subclasses__()
  for model_class in model_classes:
    if model_class.plural == plural:
      return model_class

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
      lookup_model(element.tag).from_xml(element).persist()

  def export_xml(self):
    """Exports XML from database to specified filename"""
    # Get each Model:
    model_classes = Model.__subclasses__()
    xml = XML.from_string("<WorldCrises></WorldCrises>")

    for model_class in XML_ROOT_ELEMENTS:
      records = model_class.all()
      for record in records:
        xml.tree.append(record.to_xml())

    return xml
  





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

  def export(self, filename):
    """Converts an XML object into an xml file"""
    ET.ElementTree(self.tree).write(filename, "UTF-8")

  def append(self, obj):
    """Appends an XML object into current XML's subclass"""
    self.tree.append(obj.tree)

  @classmethod
  def find_or_build_element(_class, tree, path):
    """Either finds a path in tree, or builds elements to the path. either way returns element"""
    if tree.find(path) is not None:
      return tree.find(path)
    else:
      # first, seperate out path to work on only one element:
      if path.find("/") > 0:
        path, try_again_path = path[0:path.find("/")], path[path.find("/")+1::]
      else:
        try_again_path = "."

      # create element if it needs to:
      if tree.find(path) is not None:
        element = tree.find(path)
      else:
        element = ET.SubElement(tree, path)

      return _class.find_or_build_element(element, try_again_path)






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
    if MYSQL_DEBUG:
      print query
    # Setup options:
    maxrows = options.get("maxrows", 0) # default to 0 / no max
    how     = options.get("how", 1) # default to table.column syntax

    assert str(type(self._c)) == "<type '_mysql.connection'>"

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
class Model(object):
  """
    A model is a mapper/representation of a relation. allows us to split up tasks a little easier.
    Basically, a model will be responsible for:
      - the serialization to/from xml of itself
      - persisting itself to the DB
  """  
  table_name = ""
  plural = ""
  hasMany = [] # [Model]
  keys = []
  foreign_key = ""

  def __init__(self, **params):
    """Initializes a new model with the given params"""
    self.params = {}
    for key, value in params.items():
      self.set(key, value)

  def get(self, key):
    """Get an attribute/associative model"""

    # special case for associative model:
    if key in self.hasMany and self.params.get(key) is None:
      self.params.__setitem__(key, lookup_model_from_plural(key).find("*","where "+self.foreign_key+"=\""+self.get(self.foreign_key)+"\""))
    
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
      xml = XML.from_string(xml).tree

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

  def to_xml(self, mappings = None):
    """returns xml object of model"""

    if mappings == None:
      mappings = DEFAULT_MAPPINGS[self.__class__.__name__]

    root = XML.from_string("<"+self.__class__.__name__+"></"+self.__class__.__name__+">")
    # loop through mappings
    for _map in mappings:
      _map[2].to_xml(self, root.tree, _map[0], _map[1])

    return root.tree

  @classmethod
  def all(cls, connection = None):
    """Quick hack just to be able to experiment, returns all records in table"""

    if connection == None:
      connection = DEFAULT_CONNECTION

    a = connection.query("select * from " + cls.table_name, how = 1)
    
    return cls.build_from_db_result(a)

  @classmethod
  def find(_class, project, select, connection = None):
    """Quick project/select find"""
    if connection == None:
      connection = DEFAULT_CONNECTION

    a = connection.query("select "+project+" from "+_class.table_name+" "+select)

    return _class.build_from_db_result(a)

  @classmethod
  def build_from_db_result(_class, results):
    """Returns a list of records from database +result+"""
    a = []
    for result in results:
      a.append(_class(**result))
    return a

  def persist(self, connection = None):
    """Persists model to DB, including all associationsx"""

    if connection == None:
      connection = DEFAULT_CONNECTION

    # Persist model to DB:
    connection.query("insert into `"+str(self.table_name)+"` ("+",".join(self.keys)+") values("+",".join(self.vals())+")")

    # Persist associations to DB:
    # for now, we only need to persist hasMany associations:
    for association in self.hasMany:
      for record in self.get(association):
        record.persist()

    return True


  def vals(self):
    """returns a list [in order of keys] of attribute values wrapped in quotes"""
    result = []
    for key in self.keys:
      if self.get(key) == None:
        result.append("NULL")
      else:
        result.append("\""+_mysql.escape_string(unicode(self.get(key)).encode('utf8'))+"\"")
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

    @staticmethod
    def to_xml(model, xml_element, path, key):
      # only do something if value is there:
      if model.get(key) is not None:
        # get element to add text to:
        element = XML.find_or_build_element(xml_element, path)
        element.text = model.get(key).decode('utf-8')

  class HasMany():
    """Serializer that initializes elements from a hasMany association"""
    @staticmethod
    def from_xml(model, xml_element, path, foreignModel):
      elements = xml_element.findall(path)
      if elements is not None:
        # create foreign objects
        foreign_records = []
        for e in elements:
          m = foreignModel.from_xml(e)

          assert(model.get(model.foreign_key) is not None) # the foreign key must be set first!!!
          m.set(model.foreign_key, model.get(model.foreign_key))

          foreign_records.append(m)
        # set relation on model
        model.set(foreignModel.plural, foreign_records)

    @staticmethod
    def to_xml(model, xml_element, path, foreignModel):
      # only do something if value is there:

      if model.get(foreignModel.plural) is not None:
        models = model.get(foreignModel.plural)
        # if path ends with an all delimeter, we know that we have a wrapper element
        # and therefore should create or select that element to build in
        if path[-1] == "*":
          xml_element = XML.find_or_build_element(xml_element, path[0:-2])

        if models is not None:
          for m in models:
            # for each model, append the element:
            xml_element.append(m.to_xml())

  class Attribute():
    """Simple serialize that retrieves attribute value on element, such as <element attr="val" />"""
    @staticmethod
    def from_xml(model, xml_element, path, (attribute, key)):
      # first check if looking for root element:
      element = xml_element.find(path)

      if element is not None:
        model.set(key, element.attrib.get(attribute))

    @staticmethod
    def to_xml(model, xml_element, path, (attribute, key)):
      # only do something if value is there:
      if model.get(key) is not None:
        # get element to add attribute to:
        element = XML.find_or_build_element(xml_element, path)
        element.set(attribute, model.get(key).decode('utf-8'))

  class Tag():
    """Simple serializer that retrieves tag name on element, such as <tagName/>"""
    @staticmethod
    def from_xml(model, xml_element, path, key):
      # first check if looking for root element:
      element = xml_element.find(path)

      if element is not None:
        model.set(key, element.tag)

    @staticmethod
    def to_xml(model, xml_element, path, key):
      # only do something if value is there:
      if model.get(key) is not None:
        # need to rename root (current element to value)
        xml_element.tag = model.get(key)








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
  keys = ["crisis_id", "crisisKind_id", "name", "startDate", "startTime", "endDate", "endTime", "economicImpact"]
  hasMany = ["locations","humanImpacts","resourcesNeeded","waysToHelp","relatedPeople","externalResources","relatedOrganizations"]

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
  table_name = "HumanImpacts"
  keys = ["crisis_id","number","type"]

class ResourceNeeded(Model):
  plural = "resourcesNeeded"
  table_name = "ResourcesNeeded"
  keys = ["crisis_id", "resource"]

class WaysToHelp(Model):
  plural = "waysToHelp"
  table_name = "WaysToHelp"
  foreign_key = "waysToHelp_id"
  keys = ["crisis_id","waysToHelp"]

class Organization(Model):
  plural = "organizations"
  table_name = "Organizations"
  foreign_key = "organization_id"
  keys = ["organization_id","organizationKind_id","name","history","telephone","fax","email","streetAddress","locality","region","postalCode","country"]
  hasMany = ["locations","externalResources","relatedPeople","relatedCrises"]

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
  hasMany = ["locations","externalResources","relatedPeople","relatedOrganizations"]

# call up runetime stuff:
main()
