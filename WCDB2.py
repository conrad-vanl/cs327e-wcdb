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
  "Crisis":
    """
    id char(100) NOT NULL
    PRIMARY KEY,
    name text NOT NULL,
    kind char(100) NOT NULL
    REFERENCES CrisisKind(id),
    start_date date NOT NULL,
    start_time time,
    end_date date,
    end_time time,
    economic_impact char(100) NOT NULL
    """,
  "OrganizationPerson":
    """
    id_organization char(100) NOT NULL
    REFERENCES Organization(id),
    id_person char(100) NOT NULL
    REFERENCES Person(id),
    PRIMARY KEY (id_organization, id_person)
    """,
  "CrisisOrganization":
    """
    id_crisis char(100) NOT NULL
    REFERENCES Crisis(id),
    id_organization char(100) NOT NULL
    REFERENCES Organization(id),
    PRIMARY KEY (id_crisis, id_organization)
    """,
  "PersonCrisis":
    """
    id_person char(100) NOT NULL
    REFERENCES Person(id),
    id_crisis char(100) NOT NULL
    REFERENCES Crisis(id),
    PRIMARY KEY (id_person, id_crisis)
    """,
  "Location":
    """
    id int NOT NULL AUTO_INCREMENT
    PRIMARY KEY,
    entity_type ENUM('C', 'O', 'P') NOT NULL,
    entity_id char(100) NOT NULL,
    locality char(100),
    region char(100),
    country char(100)
    """,
  "ExternalResource":
    """
    id int NOT NULL AUTO_INCREMENT
    PRIMARY KEY,
    entity_type ENUM('C', 'O', 'P') NOT NULL,
    entity_id char(100) NOT NULL,
    type ENUM('IMAGE', 'VIDEO', 'MAP', 'SOCIAL_NETWORK', 'CITATION', 'EXTERNAL_LINK') NOT NULL,
    link text NOT NULL
    """,
  "HumanImpact":
    """
    id int NOT NULL AUTO_INCREMENT
    PRIMARY KEY,
    crisis_id char(100) NOT NULL
    REFERENCES Crisis(id),
    type char(100) NOT NULL,
    number int NOT NULL
    """,
  "ResourceNeeded":
    """
    id int NOT NULL AUTO_INCREMENT
    PRIMARY KEY,
    crisis_id char(100) NOT NULL
    REFERENCES Crisis(id),
    description text
    """,
  "WaysToHelp":
    """
    id int NOT NULL AUTO_INCREMENT
    PRIMARY KEY,
    crisis_id char(100) NOT NULL
    REFERENCES Crisis(id),
    description text
    """,
  "Organization":
    """
    id char(100) NOT NULL
    PRIMARY KEY,
    name char(100) NOT NULL,
    kind char(100) NOT NULL
    REFERENCES OrganizationKind(id),
    history text NOT NULL,
    telephone char(100) NOT NULL,
    fax char(100) NOT NULL,
    email char(100) NOT NULL,
    street_address char(100) NOT NULL,
    locality char(100) NOT NULL,
    region char(100) NOT NULL,
    postal_code char(100) NOT NULL,
    country char(100) NOT NULL
    """,
  "OrganizationKind":
    """
    id char(100) NOT NULL
    PRIMARY KEY,
    name char(100) NOT NULL,
    description text NOT NULL
    """,
  "CrisisKind":
    """
    id char(100) NOT NULL
    PRIMARY KEY,
    name char(100) NOT NULL,
    description text NOT NULL
    """,
  "PersonKind":
    """
    id char(100) NOT NULL
    PRIMARY KEY,
    name char(100) NOT NULL,
    description text NOT NULL
    """,
  "Person":
    """
    id char(100) NOT NULL
    PRIMARY KEY,
    first_name char(100) NOT NULL,
    middle_name char(100),
    last_name char(100) NOT NULL,
    suffix char(100),
    kind char(100) NOT NULL
    REFERENCES PersonKind(id)
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
      (".", ("personIdent", "id"), Serializers.Attribute),
      ("Name/FirstName", "first_name", Serializers.Text),
      ("Name/LastName", "last_name", Serializers.Text),
      ("Name/MiddleName", "middle_name", Serializers.Text),
      ("Name/Suffix", "suffix", Serializers.Text),
      ("Location", Location, Serializers.HasMany),
      ("ExternalResources/*", ExternalResource, Serializers.HasMany),
      ("Kind", ("personKindIdent", "kind"), Serializers.Attribute),
      ("RelatedCrises/*", PersonCrisis, Serializers.HasMany),
      ("RelatedOrganizations/*", OrganizationPerson, Serializers.HasMany)
    ],
    "PersonCrisis": [
      (".", ("personIdent", "id_person"), Serializers.Attribute),
      (".", ("crisisIdent", "id_crisis"), Serializers.Attribute)
    ],
    "OrganizationPerson": [
      (".", ("organizationIdent", "id_organization"), Serializers.Attribute),
      (".", ("personIdent", "id_person"), Serializers.Attribute)
    ],
    "CrisisOrganization": [
      (".", ("crisisIdent", "id_crisis"), Serializers.Attribute),
      (".", ("organizationIdent", "id_organization"), Serializers.Attribute)
    ],
    "Organization": [
      (".", ("organizationIdent", "id"), Serializers.Attribute ),
      ("Name", "name", Serializers.Text),
      ("History", "history", Serializers.Text),
      ("ContactInfo/Telephone", "telephone", Serializers.Text),
      ("ContactInfo/Fax", "fax", Serializers.Text),
      ("ContactInfo/Email", "email", Serializers.Text),
      ("ContactInfo/PostalAddress/StreetAddress", "street_address", Serializers.Text),
      ("ContactInfo/PostalAddress/Locality", "locality", Serializers.Text),
      ("ContactInfo/PostalAddress/Region", "region", Serializers.Text),
      ("ContactInfo/PostalAddress/PostalCode", "postal_code", Serializers.Text),
      ("ContactInfo/PostalAddress/Country", "country", Serializers.Text),
      ("Kind", ("organizationKindIdent", "kind"), Serializers.Attribute),
      ("RelatedPersons/*", OrganizationPerson, Serializers.HasMany),
      ("RelatedCrises/*", CrisisOrganization, Serializers.HasMany),
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
      (".", "link", Serializers.Text)
    ],
    "HumanImpact": [
      ("Type", "type", Serializers.Text),
      ("Number", "number", Serializers.Text)
    ],
    "ResourceNeeded": [
      (".", "description", Serializers.Text)
    ],
    "Crisis": [
      (".", ("crisisIdent", "id"), Serializers.Attribute),
      ("Name", "name", Serializers.Text),
      ("Kind", ("crisisKindIdent", "kind"), Serializers.Attribute),
      ("Location", Location, Serializers.HasMany),
      ("StartDateTime/Date", "start_date", Serializers.Text),
      ("StartDateTime/Time", "start_time", Serializers.Text),
      ("EndDateTime/Date", "end_date", Serializers.Text),
      ("EndDateTime/Time", "end_date", Serializers.Text),
      ("HumanImpact", HumanImpact, Serializers.HasMany),
      ("EconomicImpact", "economic_impact", Serializers.Text),
      ("ResourceNeeded", ResourceNeeded, Serializers.HasMany),
      ("WaysToHelp", WaysToHelp, Serializers.HasMany),
      ("RelatedPersons/*", PersonCrisis, Serializers.HasMany),
      ("ExternalResources/*", ExternalResource, Serializers.HasMany),
      ("RelatedOrganizations/*", CrisisOrganization, Serializers.HasMany)
    ],
    "WaysToHelp": [
      (".", "description", Serializers.Text)
    ],
    "OrganizationKind": [
      (".", ("organizationKindIdent", "id"), Serializers.Attribute),
      ("Name", "name", Serializers.Text),
      ("Description", "description", Serializers.Text)
    ],
    "PersonKind": [
      (".", ("personKindIdent", "id"), Serializers.Attribute),
      ("Name", "name", Serializers.Text),
      ("Description", "description", Serializers.Text)
    ],
    "CrisisKind": [
      (".", ("crisisKindIdent", "id"), Serializers.Attribute),
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

  def __str__(self):
      return ET.tostring( self.tree )

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
    """Either finds a path in tree, or builds elements to create that path. either way returns element"""
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
  foreign_key = "id"

  instances = []

  def __init__(self, **params):
    """Initializes a new model with the given params"""
    self.params = {}
    self.is_new = True
    for key, value in params.items():
      self.set(key, value)

    self.__class__.instances.append(self)

  def get(self, key):
    """Get an attribute/associative model"""
    # special case for associative model:
    if key in self.hasMany and self.params.get(key) is None:
      # no, lets get it!
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
    #model = {}

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

    # make sure that this model is unique:
    model = model.attempt_combine()

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

  def attempt_combine(self):
    """Looks at other loaded models and affirms that this dude is unique. otherwise replaces model with the original"""
    # this will be handy when we have to start combining other groups' xml

    # iterate through all loaded records
    for record in self.__class__.instances:

      # if record has a 'copy'
      # a copy is determined by: two records that are the same relation and either have the same ID / ident or both have the same data
      if record is not self and record.__class__ is self.__class__ and self.foreign_key == record.foreign_key and ((record.get(self.__class__.foreign_key) is not None and record.get(self.__class__.foreign_key) == self.get(self.__class__.foreign_key)) or record.params == self.params):
        # we have to destroy the current record and return the older one
        self.destroy()
        return record
    return self 

  def destroy(self):
    """destroys record from instances"""
    self.__class__.instances.remove(self)

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
      # first, see if already cached/loaded:
      should_append = True
      for record in _class.instances:
        if record.params == result or record.get(_class.foreign_key) == result.get(_class.foreign_key):
          should_append = False
          a.append(record)
          break
      if should_append:
        record = _class(**result)
        record.is_new = False
        a.append(record)
    return a

  def persist(self, connection = None):
    """Persists model to DB, including all associationsx"""

    if connection == None:
      connection = DEFAULT_CONNECTION

    # Persist model to DB:
    if self.is_new or self.get(self.foreign_key) is None:
      connection.query("insert into `"+str(self.table_name)+"` ("+",".join(self.keys)+") values("+",".join(self.vals())+")")
      self.is_new = False
    else:
      print "update", self.table_name, "sql", ",".join(self.keyValueSQL()), "where", self.foreign_key, "=", self.get(self.foreign_key)
      connection.query("update `"+str(self.table_name)+"` set "+",".join(self.keyValueSQL())+" where "+self.foreign_key+"=\""+self.get(self.foreign_key)+"\"")

    # Persist associations to DB:
    # for now, we only need to persist hasMany associations:
    for association in self.hasMany:
      for record in self.get(association):
        record.persist()

    return True

  def keyValueSQL(self):
    """returns a key="value", pair for sql"""
    s = []
    for key, value in zip(self.keys, self.vals()):
      s.append(str(key)+"="+value)
    return s

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
        element.text = model.get(key)

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
  instances = []
  plural = "crises"
  table_name = "Crises"
  foreign_key = "crisis_id"
  keys = ["crisis_id", "crisisKind_id", "name", "startDate", "startTime", "endDate", "endTime", "economicImpact"]
  hasMany = ["locations","humanImpacts","resourcesNeeded","waysToHelp","relatedPeople","externalResources","relatedOrganizations"]

class RelatedPerson(Model):
  instances = []
  plural = "relatedPeople"
  table_name = "RelatedPeople"
  foreign_key = "relatedPerson_id"
  keys = ["person_id","crisis_id","organization_id"]

class RelatedOrganization(Model):
  instances = []
  plural = "relatedOrganizations"
  table_name = "RelatedOrganizations"
  foreign_key = "relatedOrganization_id"
  keys = ["person_id","crisis_id","organization_id"]

class RelatedCrisis(Model):
  instances = []
  plural = "relatedCrises"
  table_name = "RelatedCrises"
  foreign_key = "relatedCrisis_id"
  keys = ["person_id","crisis_id","organization_id"]

class Location(Model):
  instances = []
  plural = "locations"
  table_name = "Locations"
  foreign_key = "location_id"
  keys = ["crisis_id","person_id","organization_id","locality","region","country"]

class ExternalResource(Model):
  instances = []
  plural = "externalResources"
  table_name= "ExternalResources"
  foreign_key = "externalResource_id"
  keys = ["crisis_id","organization_id","type","content"]

class HumanImpact(Model):
  instances = []
  plural = "humanImpacts"
  table_name = "HumanImpacts"
  foreign_key = "humanImpact_id"
  keys = ["crisis_id","number","type"]

class ResourceNeeded(Model):
  instances = []
  plural = "resourcesNeeded"
  table_name = "ResourcesNeeded"
  foreign_key = "resourceNeeded_id"
  keys = ["crisis_id", "resource"]

class WaysToHelp(Model):
  instances = []
  plural = "waysToHelp"
  table_name = "WaysToHelp"
  foreign_key = "waysToHelp_id"
  keys = ["crisis_id","waysToHelp"]

class Organization(Model):
  instances = []
  plural = "organizations"
  table_name = "Organizations"
  foreign_key = "organization_id"
  keys = ["organization_id","organizationKind_id","name","history","telephone","fax","email","streetAddress","locality","region","postalCode","country"]
  hasMany = ["locations","externalResources","relatedPeople","relatedCrises"]

class OrganizationKind(Model):
  instances = []
  plural = "organizationKinds"
  table_name = "OrganizationKinds"
  foreign_key = "organizationKind_id"
  keys = ["organizationKind_id","name","description"]

class CrisisKind(Model):
  instances = []
  plural = "crisisKinds"
  table_name = "CrisisKinds"
  foreign_key = "crisisKind_id"
  keys = ["crisisKind_id","name","description"]

class PersonKind(Model):
  instances = []
  plural = "personKinds"
  table_name = "PersonKinds"
  foreign_key = "personKind_id"
  keys = ["personKind_id","name","description"]

class Person(Model):
  instances = []
  plural = "people"
  table_name = "People"
  foreign_key = "person_id"
  keys = ["person_id","firstName","lastName","middleName","suffix","personKind_id"]
  hasMany = ["locations","externalResources","relatedPeople","relatedOrganizations"]

# call up runetime stuff:
main()
