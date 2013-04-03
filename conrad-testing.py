import WCDB2

# setup factory:
factory = WCDB2.Factory()

print "###### Factory: ######"
print factory
print "\n"

# setup XML:
xml_string = """
<WorldCrises>
 <Person personIdent="BTownsend">
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
</WorldCrises>
"""

xml = WCDB2.XML.from_string(xml_string)

print "###### XML: ######"
print xml
print "\n"


# test serializing XML:
factory.import_xml(xml)

