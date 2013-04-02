require "builder"
require "faker"

module Generator
  @@fake = {
    "city"=>"Faker::Address","country"=>"Faker::Address","latitude"=>"Faker::Address","longitude"=>"Faker::Address","state"=>"Faker::Address","street_name"=>"Faker::Address","street_address"=>"Faker::Address","zip_code"=>"Faker::Address",
    "bs"=>"Faker::Company","catch_phrase"=>"Faker::Company","name"=>"Faker::Company","suffix"=>"Faker::Company",
    "domain_name"=>"Faker::Internet","url"=>"Faker::Internet","email"=>"Faker::Internet",
    "first_name"=>"Faker::Name","last_name"=>"Faker::Name"
  }
  @@fake_keys = @@fake.keys

  # +n+ number of child elements
  def self.produce_random_xml (n)
    xml = Builder::XmlMarkup.new( :indent => 2 )
    
    xml.root do |p|
      n.to_i.times do |i|
        create_children p, n, i
      end
    end

    return xml
  end
    
  def self.create_children (tag, n, i)
    levels = n - i # * rand(i..n)
    if levels <= 1
      tag.text! Faker::Lorem.paragraph
    else
      levels.to_i.times do |ii|
        tag.tag! random_tag(), random_attributes(n, i).to_hash do |p|
          create_children(p, levels, i+1)
        end
      end
    end
  end


  def self.random_tag
    #key = @@fake_keys[ rand(@@fake_keys.length) ]
    #return eval("#{@@fake[key]}.#{key}")
    @@fake_keys[ rand(@@fake_keys.length) ]
  end

  def self.random_attributes(n, i)
    att = {}
    r = rand(i..n)

    if !r.nil?
      r.times do |b|
        tag = random_tag()
        att[tag] = eval("#{@@fake[tag]}.#{tag}")
      end
    end

    return att
  end


  def self.generate_file(filename, i)
    File.open(filename, 'w') do |file|
      file.write produce_random_xml(i)
    end
  end
end

Generator.generate_file "TestWCDB1.in.xml", 10