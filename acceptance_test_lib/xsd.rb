require "rexml/document"
require "acceptance_test_lib/element"
require "acceptance_test_lib/types"
require "acceptance_test_lib/groupitemloader"
require "acceptance_test_lib/content"



module XSDInfo


   class SchemaCollection
     def inspect 
         return to_s
     end

     def initialize
        @schemas = Hash.new
     end
 
     def add_schema s
        @schemas[s.target_namespace] = s
     end

     def get_element (ns,name)
        result = nil        
        if @schemas[ns] then
           result = @schemas[ns].elements[name]
        end 
        return result
     end

     def get_type (ns,name) 
        result = nil
        if @schemas[ns] then
           result = @schemas[ns].types[name]
        end 
        return result
     end

     def get_group(ns,name) 
        result = nil
        if @schemas[ns] then
           result = @schemas[ns].groups[name]
        end 
        return result
     end

     def get_attribute_group(ns,name) 
        result = nil
        if @schemas[ns] then
           result = @schemas[ns].attribute_groups[name]
        end 
        return result
     end

     def namespaces
       @schemas.keys
     end

     def [](x)
        @schemas[x]
     end

   end

   class SchemaInformation
      def inspect
        return "(#{to_s} #{@filename}:#{@targetNamespace})"
      end

      @filename = ""
      @targetNamespace = ""
      @elementForDefault = :qualified
      @prefixes = Hash.new
      @elements = Hash.new
      @attribute_groups = Hash.new
      @groups = Hash.new

      def initialize(filename) 
         @filename = filename
        file = File.new(filename)
         doc = REXML::Document.new file
         processAttributes doc.root.attributes
         processContent doc.root.children
      end

      def solve_references(collection)
        [@attribute_groups,@types,@groups,@elements].each { |m|
          m.values.each{|e| e.solve_references(collection)}
        }
      end

      def target_namespace()
         return @targetNamespace
      end
      
      def printt()
        print "#{@targetNamespace},#{@filename},#{@a}\n"
      end

      def elements()
        return @elements
      end 

      def types()
        return @types
      end

      def attribute_groups()
        return @attribute_groups
      end

      def groups
         return @groups
      end

      def prefixes
          return @prefixes
      end

      private 

      def processAttributes(attributes)
        @targetNamespace = attributes["targetNamespace"]
        if (attributes["elementFormDefault"] == "qualified") then
            @elementFormDefault = :qualified
        else
            @elementFormDefault = :unqualified
        end
        @prefixes = Hash.new
        attributes.values.each{
             |attribute|
             if attribute.prefix == "xmlns" then
                @prefixes[attribute.name] = attribute.value
             end
        }
        if (default_namespace = attributes["xmlns"]) then
           @prefixes["__default__"] = default_namespace
        end
      end
 
      def processContent(elements)
        @elements = Hash.new
        @types = Hash.new
        @groups = Hash.new
        @attribute_groups = Hash.new

        elements.find_all {|e| e.class == REXML::Element }.each {|x| processElement x}
      end
      def processElement(element) 
         case element.name
            when "element"
               processSchemaElement(element)
            when "complexType"
               processComplexType(element)
            when "attributeGroup" 
               processAttributeGroup(element)
            when "group"
               processGroup(element)
            else
              print "Warning: ignoring #{element}"
         end
      end
      

      def processSchemaElement(elementDefinition)
          e = SchemaElement.new()
          e.load_from(elementDefinition,@prefixes)
          @elements[e.name] = e
      end

      def processComplexType(complexTypeElement) 
         ct = SchemaComplexType.new
         ct.load_from(complexTypeElement,@prefixes)
         @types[ct.get_name] = ct 
      end
 
      def processAttributeGroup(element)
        ag = SchemaAttributeGroup.new
        ag.load_from(element,@prefixes)
        @attribute_groups[ag.name] = ag
      end

      def processGroup(element)
        g = SchemaGroup.new
        g.load_from(element,@prefixes)
        @groups[g.name] = g
      end
   end

   class SchemaAttributeGroup
      attr_reader :name
      attr_reader :attributes
      attr_reader :attribute_groups

      def inspect
        return "(#{to_s} #{@name})"
      end

      def load_from(element,prefixes)
        @name = element.attributes["name"]
        @attributes = Hash.new
        @attribute_groups = Hash.new
        element.children.find_all{|e| !e.is_a? REXML::Text}.each{|e|
            case e.name
            when "attribute"
                 att = SchemaAttribute.new
                 att.load_from(e,prefixes)
                 @attributes[att.name] = att
            when "attributeGroup"
                 agRef = Reference.new(e.attributes["ref"],prefixes)
                 @attribute_groups[agRef.name] = agRef 
            else
              print "Warning: ignoring #{e}"
            end
        }
      end
      def solve_references(c)
        vals = @attribute_groups.values
        vals.find_all{|x| x.is_a? Reference}.each {|ag|
           solved_ag = c.get_attribute_group(ag.namespace,ag.name)
           @attribute_groups[solved_ag.name] =  solved_ag unless solved_ag == nil
        }
      end

      def all_attributes()
        return @attributes.values + 
               @attribute_groups.values.collect {|ag| ag.all_attributes}.flatten
      end
   end






   class SchemaAttribute
      def load_from(element,prefixes)
         @name = element.attributes["name"]
         
         if (element.attributes["type"]) then
         
           @atype = Reference.new(element.attributes["type"],prefixes)
         end

         if(element.attributes["required"] == "true") then
           @required = true
         else
           @required = false
         end       
      end

      def name()
         return @name
      end

      def attribute_type() 
         return @atype
      end

      def required?()
        return @required
      end
   end

   class Reference
      attr_accessor :name
      attr_accessor :namespace
      def initialize(reference,prefixes)
        s = reference.split(":")
        if (s.length > 1) then
          if (ns = prefixes[s[0]]) then
             @namespace = ns
          else
             @namespace = s[0]
          end
          @name = s[1]
        else
           @namespace = prefixes["__default__"]
           @name = reference
        end
        
      end

      def all_attributes()
        print "unsolved reference: #{@namespace}:#{@name}"
        raise "error"
      end
   end

end


