import WCDB3

WCDB3.MYSQL_DEBUG = True

f = WCDB3.Factory()
f.import_xml( WCDB3.XML.from_file("instance.xml") )

xml = f.export_xml()

xml.export("test2.xml")