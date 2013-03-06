require "rexml/document"
require "acceptance_test_lib/xsd"
require "acceptance_test_lib/groupitemloader"

module XSDInfo
   class SchemaType
      def inspect
        return "#{to_s}"
      end
      def solve_references(sc)
        print "Warning: Method not implemented in #{self.class} \n"
      end

      def all_attributes
         return []
      end

   end

   class SchemaSimpleType < SchemaType
   end

   class SchemaComplexType < SchemaType
      include GroupItemLoader

      @name = "" 
      
      @attributes = Hash.new
      def get_name()
        return @name
      end

      def load_from(complexTypeElement,prefixes)        
         if (complexTypeElement.attributes["name"]) then
           @name = (complexTypeElement.attributes["name"])
         end

         if (complexTypeElement.attributes["mixed"] == "true") then
            @mixed = true
         else
            @mixed = false
         end

         @attributes = Hash.new
         @attribute_groups = Hash.new
         @complexContent = nil
         @contentParts = []
         complexTypeElement.children.find_all {|e| e.class == REXML::Element}.
          each {
           |e|
               if (loaded = load_group_item(e,prefixes))
                  @contentParts = @contentParts + [loaded]
               else
                  case e.name
                    when "attribute"
                       att = SchemaAttribute.new
                       att.load_from(e,prefixes)
                       @attributes[att.name] = att
                    when "attributeGroup"
                       agRef = Reference.new(e.attributes["ref"],prefixes)
                       @attribute_groups[agRef.name] = agRef 
                    when "complexContent"
                       cc = SchemaComplexContent.new
                       cc.load_from(e,prefixes)
                       @complexContent = cc
                    else 
                       print "Warning: ignoring #{e}"
                 end
               end
           }

      end

      def complex_content
         return @complexContent
      end

      def content  
          return @contentParts
      end
      
      def all_content_parts
         result = @contentParts
         result = (@complexContent.all_content_parts + result) unless @complexContent == nil
         return result
      end


      def all_attributes
         result = @attributes.values
         result = result + @attribute_groups.values.collect {|x| x.all_attributes}.flatten
         if (@complexContent != nil) then
            result = result + @complexContent.all_attributes
         end
         return result
      end

      @solving = false
      def solve_references(sc)
        @complexContent.solve_references(sc) unless @complexContent == nil
        agroups = @attribute_groups.values
        agroups.find_all{|x| x.is_a? Reference}.each {|ag|
              solved_tag  = sc.get_attribute_group(ag.namespace,ag.name)
              @attribute_groups[solved_tag.name] = solved_tag unless solved_tag == nil
         }
        if !@solving then
           @solving = true
           @contentParts.each{|x| x.solve_references sc}
           @solving = false
        end
      end

      ## Sample Generation

      def generate_sample_content(e,context)
        atts = all_attributes.select {|x| x.name != nil && rand > 0.7}
        atts.each {|att|
          sample_length = 1 + (10*rand).to_i
          sample_text = (1..sample_length).to_a.collect{ |p| 
              ltrs = ("a"[0].."z"[0]).to_a
              ltrs[(ltrs.length*rand).to_i]
             }.pack("c"*sample_length)
          e.attributes[att.name] = sample_text
        } 

        self.all_content_parts.each {|p| p.generate_sample_content(e,context)}
      end


   end



end
