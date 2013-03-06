require "rexml/document"
require "acceptance_test_lib/xsd"

module XSDInfo

   class SchemaElement
      attr_reader :name

      def inspect
        return "#{to_s} #{@name}"
      end
      def load_from(elementDefinition,prefixes)
          
         @name = elementDefinition.attributes["name"]
         if (elementDefinition.attributes["type"]) then
             @element_type = Reference.new(elementDefinition.attributes["type"],prefixes)
         end          
         if (elementDefinition.attributes["substitutionGroup"]) then
             @substitution_group = Reference.new(elementDefinition.attributes["substitutionGroup"],prefixes)
         end          

         elementDefinition.find_all {|e| !e.is_a?(REXML::Text)}.each{|e|
              case e.name
                  when "complexType" 
                      ct = SchemaComplexType.new
                      ct.load_from(e,prefixes)
                      @element_type = ct
                  else
                      print "Warning: ignoring #{e}"
              end
         }

      end

      def set_type (elementType)
        @element_type = elementType
      end
      def set_substitution_group(subsGroup) 
        @substitution_group = subsGroup
      end
      def element_type()
         return @element_type
      end
      def substitution_group()
          return @substitution_group
      end

      @solving = false
      def solve_references(collection)
        if @substitution_group.is_a?(XSDInfo::Reference) then
           @substitution_group = collection.get_type(
                                      @substitution_group.namespace,
                                      @substitution_group.name)
        end

        if @element_type.is_a?(XSDInfo::Reference) then
           if(r = collection.get_type(@element_type.namespace,@element_type.name)) then
              @element_type = r
           else
             print "Not found #{@element_type.namespace}.#{@element_type.name}\n"
           end
        else         
           if !@solving then
              @solving = true
              @element_type.solve_references(collection) unless @element_type == nil
              @solving = false
           end
        end
      end

      def all_attributes
        if (@element_type != nil) then
           return @element_type.all_attributes
        else
           return []
        end
      end

      ## Sample generation
      def a_sample
        return generate_sample(nil,Hash.new)
      end

      def generate_sample(p,context)
         if(!(context.has_key? @name) ||
            (context[@name] < 2)) then

             if (!context.has_key? @name) then
                context[@name] = 1
             else
                context[@name] = context[@name]+1
             end
             print "Generating for #{@name}\n"
             e = REXML::Element.new(@name)
             @element_type.generate_sample_content(e,context) unless @element_type == nil
             if (p != nil) then
                p.elements << e
             end
             return e
         end
      end
   end
  


end
