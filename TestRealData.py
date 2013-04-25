import WCDB3

WCDB3.MYSQL_DEBUG = True

f = WCDB3.Factory()

files = [
  "better.xml",
  "biteme.xml",
  "bonsai.xml",
  "miner.xml",
  "poseidon.xml",
  "techsupport.xml",
  "virus.xml",
  "yuchen.xml",
  "WCDB3.xml"
]


for name in files:
  f.import_xml( WCDB3.XML.from_file(name) )

xml = f.export_xml()

xml.export("TestRealData.xml")