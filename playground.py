"""
  Just messing around with API ideas, trying to figure out best way to code out everything
"""

import WCDB2



# Playing around with Models
org = WCDB2.Organization()

# setting a direct attribute:
org.name = "My Fancy Organization"

# how to set a foreign attribute / associated model?
# org.organizationKind = ??

  # OPTION 1: (FAVORING THIS OPTION)
  # setup the association first, then link to it:
  orgKind = WCDB2.OrganizationKind(name = "Relief", description = "A relief organization")
  org.organizationKind = orgKind

  # OPTION 2: 
  # Same as option 1, but set by setting foreignKey:
  # orgKind = WCDB2.OrganizationKind(name = "Relief", description = "A relief organization")
  # org.organizationKind_id = orgKind.organizationKind_id

  # OPTION 3:
  # dynamically assign/create associations:
  # org.organizationKind = { "name": "Relief", "description": "A relief organization" }



# OKay, so what about processing XML?
# Well, if the models are done right, it *should* be as easy as loading up some sort of serializer
# or mapping that takes an XML resource and converts it to a hash and then iterate over the hash and set 
# params in the relation:

xml_string = """
<WorldCrises>
 <Person>
   <Name>
     <FirstName>Bob</FirstName>
     <LastName>Townsend</LastName>
   </Name>
   <Location>
      <Locality>Washington</Locality>
      <Region>D.C.</Region>
      <Country>United States</Country>
    </Location>
   <kind personKindIdent="LD"/>
 </Person>
 <PersonKind personKindIdent="LD">
   <Name>Leader</Name>
   <Description>Leader of an organization</Description>
 </PersonKind>
</WorldCrises>
"""
xml = WCDB2.XML.from_string(xml_string)

# What if we can map this XML to something that is easier to work with?
map_result = [
  { "person": {
    "firstName":"Bob",
    "lastName":"Townsend",
    "locations": [
      {
        "locality": "Washington",
        "region": "D.C.",
        "country": "United States"
      }
    ],
    "personKind_id": "LD",
  } },
  { "personKind": {
   "personKind_id": "LD",
   "name": "leader",
   "description": "Leader of an organization" 
  } }
]
# then we can just loop over each dict in the list and create that element from params

# so how do we create this list of hashes?
# Basic idea: loop over root elements in XML and apply some sort of mapping function:
for element in xml: # should just loop over first level of elements
  Models.lookup(element.tag).from_xml(element)

  # (that's the same as doing say)
  # WCDB2.Person.from_xml(element)

# from_xml pseudo-code:
MAPPING_XML = [
 ("Name.FirstName", "firstName", Serializers.Text),
 ("Name.LastName", "lastName", Serializers.Text),
 ("Location", Location, Serializers.HasMany), # HAS_MANY associations are passed so that they can be initialized on their own?
 ("Kind", ("personKindIdent", "personkind_id"), Serializers.Attribute)
]

class Model():
  @classmethod
  def from_xml(_class, xml_element):
    # initialize empty model:
    model = _class()

    for _map in MAPPING_XML:
      # _map is a tuple
      # first element is XML +path+
      # second element is either:
      #   string: key                       => key = xml_element.find(path).text()
      #   modelClass: HAS_MANY association  => key = modelClass.plural() = **create each from_xml and return array: xml_element.findAll(path)**
      #   tuple: (attribute, key)           => key = xml_element.find(path).get(attribute)
      # third element is the serialization function to be used
      _map[2].from_xml(model, xml_element, _map[0], _map[1])

    return model

class Serializers():
  class Text():
    """Simple serializer that retrieves text value on element, such as <element>text value</element>"""
    @classmethod
    def from_xml(model, xml_element, path, key):
      element = xml_element.find(path)
      if element:
        model.set(key, element.text())

  class HasMany():
    """Serializer that initializes elements from a hasMany association"""
    @classmethod
    def from_xml(model, xml_element, path, foreignModel):
      elements = xml_element.findAll(path)
      if elements:
        # create foreign objects
        foreign_records = []
        for e in elements:
          foreign_records.append(foreignModel.from_xml(e))
        # set relation on model
        model.set(foreignModel.plural, foreign_records)

  class Attribute():
    """Simple serialize that retrieves attribute value on element, such as <element attr="val" />"""
    @classmethod
    def from_xml(model, xml_element, path, (attribute, key)):
      element = xml_element.find(path)
      if element:
        model.set(key, element.attrib.get(attribute))