require "rexml/document"
require "acceptance_test_lib/xsd"
require "acceptance_test_lib/groupitemloader"

module XSDInfo

   class SchemaContentElement 

       attr_reader :minOccurs
       attr_reader :maxOccurs

       def inspect
          return to_s
       end

       def load_occurs(e)
          minOccurs = e.attributes["minOccurs"]
          if minOccurs == nil then 
            minOccurs = 1 
          else
            minOccurs = minOccurs.to_i
          end

          maxOccurs = e.attributes["maxOccurs"]
          if maxOccurs == nil then 
            maxOccurs = 1 
          else
              maxOccurs = maxOccurs.to_i unless maxOccurs == "unbounded"
          end
          return [minOccurs,maxOccurs] 
       end

       def load_from_occurs(e,prefixes)
           occ = load_occurs(e)
           @minOccurs = occ[0]
           @maxOccurs = occ[1]
       end
     
       def generate_sample_content (e,c)
          #not implemented
       end

   end



   class SchemaElementGroup < SchemaContentElement
       attr_reader :elements
     
       include GroupItemLoader
   
       def load_from(e,prefixes)
         load_from_occurs(e,prefixes)
         @elements = []                
         e.children.find_all {|e| !e.is_a? REXML::Text}.each {|e|
            if item = load_group_item(e,prefixes)
              @elements = @elements + [item]
            else
              print "Warning: ignoring #{e}"
            end
         }
       end

       @solving = false

       def solve_references(c)
         if !@solving then
            @solving = true
            @elements = @elements.collect {|e|  
                if (e.is_a? Reference) then
                   c.get_group(e.namespace,e.name)
                else
                   e.solve_references(c)
                   e
                end
             }
             @solving = false
         else
           print "Skipping!!!\n"
         end

       end

      ## Sample generation

       def generate_sample_content(e,context)
          if (@minOccurs == 1 && @maxOccurs == 1) then
            @elements.each{|edef|
             edef.generate_sample_content(e,context)
            }
          elsif (@minOccurs == 0 && @maxOccurs == 1) then
            @elements.each{|edef|
              edef.generate_sample_content(e,context) 
            } unless rand < 0.5              
          elsif (@maxOccurs == "unbounded") then
             (1..(rand * 4).to_i).each {|i|
                @elements.each{|edef|
                   edef.generate_sample_content(e,context)
                } unless rand < 0.5              
             }
          end          
       end

   end


   class SchemaInternalElement < SchemaContentElement
      attr_reader :element
      def load_from(e,prefixes)
          load_from_occurs(e,prefixes)
          if e.attributes.has_key? "ref"
              eref = Reference.new(e.attributes["ref"],prefixes)
              @element = eref
           else
              inline_element = SchemaElement.new
              inline_element.load_from(e,prefixes)
              @element = inline_element
           end
                  
      end
      def solve_references(c)
        if @element.is_a? Reference then
           @element = c.get_element(@element.namespace,@element.name)
        end 
      end


       ## Sample generation

       def generate_sample_content(e,context)
          if (@minOccurs == 1 && @maxOccurs == 1) then
              @element.generate_sample(e,context)
          elsif (@minOccurs == 0 && @maxOccurs == 1) then
              @element.generate_sample(e,context) unless rand < 0.5
          elsif (@maxOccurs == "unbounded") then
             (1..(rand * 4).to_i).each {|i|
                 @element.generate_sample(e,context)
             }
          end
          
       end
   end

   class SchemaSequence < SchemaElementGroup
 
   end

   class SchemaChoice < SchemaElementGroup
      ## Sample generation

       def generate_sample_content(e,context)
          if (@minOccurs == 1 && @maxOccurs == 1) then
            element_to_gen = @elements[(rand*@elements.length).to_i]
            element_to_gen.generate_sample_content(e,context)
          elsif (@minOccurs == 0 && @maxOccurs == 1) then
            element_to_gen = @elements[(rand*@elements.length).to_i]
            element_to_gen.generate_sample_content(e,context) unless rand < 0.5    
          elsif (@maxOccurs == "unbounded") then
             (1..(rand * 4).to_i).each {|i|
                  element_to_gen = @elements[(rand*@elements.length).to_i]
                  element_to_gen.generate_sample_content(e,context) unless rand < 0.5             
             }
          end          
       end
   end

   class SchemaGroup < SchemaElementGroup
      attr_reader :name
      def load_from(e,prefixes)
         super(e,prefixes)
         @name = e.attributes["name"]
      end
   end



   class SchemaComplexContent
     @extension = nil
     def load_from(element,prefixes)
       element.children.find_all{|x| x.is_a? REXML::Element}.each {|e|
          case e.name
            when "extension"
              @extension = SchemaExtension.new
              @extension.load_from(e,prefixes)
            else
              print "Warning: Ignoring #{e}"                      
         end
       }
     end
     def extension()
        return @extension
     end

     def all_content_parts
       result = []
       result = @extension.all_content_parts unless @extension == nil 
       return result
     end

     def all_attributes
        return @extension.all_attributes
     end

     def solve_references(c)
        @extension.solve_references(c) unless @extension == nil
     end
   end
   
   class SchemaExtension
       include GroupItemLoader

       def inspect
         return to_s
       end

       def load_from(element,prefixes)
          @attributes = Hash.new
          @attribute_groups = Hash.new
          @base = Reference.new(element.attributes["base"],prefixes)
          @contentParts = []
          element.children.find_all {|x| x.is_a? REXML::Element }.each{|e|
            if (item = load_group_item(e,prefixes))
              @contentParts = @contentParts + [item]
            else
              case e.name
                when "attribute"
                  att = SchemaAttribute.new
                  att.load_from(e,prefixes)
                  @attributes[att.name] = att
                when "attributeGroup"
                  agRef = Reference.new(e.attributes["ref"],prefixes)
                  @attribute_groups[agRef.name] = agRef 
                else  
                  print "Warning: Ignoring #{e}"
              end
            end
          }
       end

       def all_content_parts
          result = @contentParts
          result = @base.all_content_parts +  result unless @base == nil
          return result
       end

       def all_attributes
           result = @attributes.values
           result = result + 
                    @attribute_groups.values.collect {|x| x.all_attributes}.flatten
           if (@base.is_a?(SchemaComplexType)) then
              result = result + @base.all_attributes
           end
          return result
       end 
 
       def solve_references(c)
            if (@base.is_a?(XSDInfo::Reference)) then               
               if (r = c.get_type(@base.namespace,@base.name)) then
                  @base = r
               else
                 print "Could not find #{@base.namespace}:#{@base.name} #{@base.namespace.class} #{@base.name.class}\n"
               end
            end
            agroups = @attribute_groups.values
            agroups.find_all{|x| x.is_a? Reference}.each {|ag|
              solved_tag  = c.get_attribute_group(ag.namespace,ag.name)
              @attribute_groups[solved_tag.name] = solved_tag unless solved_tag == nil
         }
  
       end
   end
  


end
