# lets grab the library
import WCDB2

# turn on MySQL debugging:
print "TURNING ON MYSQL DEBUGGING"
WCDB2.MYSQL_DEBUG = True

factory1 = WCDB2.Factory()

# import
xml = WCDB2.XML.from_file("RunWCDB2.in.xml")
factory1.import_xml(xml)

# export
out_xml = factory1.export_xml()
out_xml.export("RunWCDB2.out.xml")

# check for equality
# we know have xml and out_xml, and need to check for equality
# we can loop through one xml, and see if each element exists in the new xml:

tests = True
for element in xml.tree.iter():
  print "\n", "TEST:", element
  we_won = False
  # special case for empty elements (they shouldn't be in the new xml anyways)
  if element.text is None and not len(element.attrib):
    print "   EMPTY ELEMENT. MOVING ON."
  else:
    for potential_find in out_xml.tree.iter(element.tag):
      print "  TRY: ", element, potential_find, element.tag == potential_find.tag, element.attrib == potential_find.attrib
      if element.tag == potential_find.tag and element.attrib == potential_find.attrib:
        we_won = True
        break
    
    if not we_won:
      tests = False
      print "FAIL!"
      print WCDB2.ET.tostring(element), "\n\n" 

if not tests:
  print "There were failing tests. FAIL!"
else:
  print "ALL TESTS PASS! WE WON!"

"""
factory2 = WCDB2.Factory()


# importing the export and re-exporting it
factory2.import_xml(out_xml)
out2_xml = factory2.export_xml()
out2_xml.export("RunWCDB2data2.out.xml")

file1 = open("RunWCDB2.out.xml", 'r')
file2 = open("RunWCDB2data2.out.xml", 'r')

# comparing the initial export with its own export

file1xml = []
file2xml = []

for line in file1:
    file1xml.append(line)
for line in file2:
    file2xml.append(line)

flag = True

for line in file1xml:
    if line not in file2xml:
        flag = False
        break
    else:
        pass
    
assert flag
"""
# done!
