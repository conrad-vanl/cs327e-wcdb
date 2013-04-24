import WCDB3

WCDB3.MYSQL_DEBUG = True

f = WCDB3.Factory()
f.import_xml( WCDB3.XML.from_file("WCDB3.xml") )

xml = f.export_xml()

xml.export("WCDB3.out.xml")