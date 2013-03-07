require "builder"

@@tag_names = ["apple","banana","cabana","bluetooth","carl","team","monday","tuesday","foggy","cloudy","windy","rainy","taco","burrito","gordita","salad","ranch","boss","associate","brandice","bellatrice","beatrice","conrad","red","yellow","green","blue","orange"]


# +n+ number of child elements
def produce_random_xml (n)
  xml = Builder::XmlMarkup.new( :indent => 2 )
  
  xml.root do |p|
    n.to_i.times do |i|
      create_children p, n, i+1
    end
  end

  return xml
end
  
def create_children (tag, n, i)
  levels = n - i # * rand(i..n)
  if levels == 1
    p.text! random_tag()
  else
    levels.to_i.times do |ii|
      tag.tag! random_tag(), randrom_attributes(n, i) do |p|
        create_children(p, levels, i + 1)
      end
    end
  end
end


def random_tag
  @@tag_names[ rand(@@tag_names.length) ]
end

def random_attributes(n, i)
  att = {}
  rand(n..i).times.do |b|
      att[random_tag()] = random_tag()
  end
end


def generate_file(filename, num_tests, seed)
  File.open(filename, 'w') do |file|
    num_tests.to_i.times do |i|
      file.write produce_random_xml(rand(i..seed))
      file.write "\n"
    end
  end
end