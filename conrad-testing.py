import WCDB2

WCDB2.MYSQL_DEBUG = True

f = WCDB2.Factory()
f.import_xml( WCDB2.XML.from_file("instance.xml") )

xml = f.export_xml()

xml.export("test.xml")