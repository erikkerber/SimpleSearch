module InformationRetrieval
  class Document
    
    """
  	Object represeting a document or query.

  	name: 		filename of the document
  	document: 	raw list of words in original order.
  	word_count:	hash of each word and how many times that word appears.
  	word_tf:	hash of each word and it's respective tf value.

  	"""
  	def initialize(filename)
	    begin
	      doc = File.open(filename).read()
      rescue
        print 'Could not open file ', filename
      end
      
      @name = filename
      @document = doc.split()
      @word_count = count_words
	    
	  end
    
    def count_words
      print 'Counting words!'
    end
    private :count_words
    
    def get_tf
      
    end
    private :get_tf
  end
end

a = InformationRetrieval::Document.new('Test/D1.txt')
