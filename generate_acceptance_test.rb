$LOAD_PATH << File.dirname(__FILE__) + "/"
require "acceptance_test_lib/xsd"


def generate_sample ( schema, root, filename )
      sc = XSDInfo::SchemaCollection.new
      sc.add_schema XSDInfo::SchemaInformation.new("./"+schema)
      sc.namespaces.each {|ns| sc[ns].solve_references sc}
      doc = REXML::Document.new
      f = File.new(filename,"w")
      doc.elements << sc[sc.namespaces[0]].elements[root].a_sample
      doc.write(f)
      f.close
      return sc
end


def generate_sample_element name, schema, filename
      sc = XSDInfo::SchemaCollection.new
      sc.add_schema XSDInfo::SchemaInformation.new("./"+schema)
      sc.namespaces.each {|ns| sc[ns].solve_references sc}
      doc = REXML::Document.new
      f = File.new(filename,"w")
      doc.elements << sc[sc.namespaces[0]].elements[name].a_sample
      doc.write(f,3,false,false)
      f.close
      return sc
end