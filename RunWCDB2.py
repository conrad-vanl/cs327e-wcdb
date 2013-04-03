# lets grab the library
from WCDB2 import *

# import
data = WCDB2.XML.from_file("RunWCDB2.in.xml")

# export
data.export("RunWCDB2.out.xml")

# importing the export and re-exporting it
data2 = WCDB2.XML.from_file("RunWCDB2.out.xml")
data2.export("RunWCDB2data2.out.xml")

file1 = open("RunWCDB2.out.xml", 'r')
file2 = open("RunWCDB2data2.out.xml", 'r')

# comparing the initial export with its own export

file1xml = ""
file2xml = ""

for line in file1:
    file1xml += line
for line in file2:
    file2xml +=line

assert file1xml == file2xml

# done!
