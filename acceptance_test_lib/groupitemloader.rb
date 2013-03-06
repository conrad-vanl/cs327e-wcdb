require "rexml/document"
require "acceptance_test_lib/xsd"


module XSDInfo
    module GroupItemLoader
       def load_group_item(e,prefixes)
           result = nil
           case e.name
               when "element"
                  result = SchemaInternalElement.new
                  result.load_from(e,prefixes)
               when "sequence"
                  seq = SchemaSequence.new
                  seq.load_from(e,prefixes)
                  result = seq
               when "choice"
                  ch = SchemaChoice.new
                  ch.load_from(e,prefixes)
                  result = ch
               when "group"
                  if e.attributes.has_key? "ref"
                     gr = Reference.new(e.attributes["ref"],prefixes)
                     result = gr
                  else
                    print "Warning: Inline group not supported #{e}"
                  end
               else
                  result = nil
            end
            return result
       end
   end

end
