# lets grab the library
from WCDB1 import *

# import
data = WCDB1.XML.from_file("RunWCDB1.in.xml")

# export
data.export("RunWCDB1.out.xml")

# done!