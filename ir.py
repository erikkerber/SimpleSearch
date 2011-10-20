from collections import defaultdict
import math
import re

class Document:
	
	"""
	Object represeting a document or query.
	
	name: 		filename of the document
	document: 	raw list of words in original order.
	word_count:	hash of each word and how many times that word appears.
	word_tf:	hash of each word and it's respective tf value.
	 
	"""
	name = ''
	document = None
	word_count = None
	word_tf = None
	
	def __init__(self, name):
		try:
			doc = open(name).read()
		except:
			doc = name + '\n' # Hack so that \W+ works for single word.

		self.name = name	
		
		# Raw original source
		self.source = doc
		
		# Split the document into a list of words
		self.document = re.split('\W', str.lower(doc))
		
		# Pop off the always-empty-last-element. I am still stupid at Python.
		self.document.pop()
		
		# Count the words into a hash
		self.word_count = self._count_words(self.document)
		
		# Now that all the words are counted, calculate each words tf.
		self.word_tf = self._get_tf(max(self.word_count.values()))
		
	# Turns a document into a dictionary of words with the frequency of those words.
	# Additionally, it returns the maximum count of any given word.
	def _count_words(self, document):
		word_count = defaultdict(int)
		for word in document:
			word_count[word] += 1
		return word_count
		
	# tf= (term count in a document)/(largest term count in a document)
	def _get_tf(self, max):
		word_tf = defaultdict(float)
		for word in self.word_count:
			word_tf[word] = float(self.word_count[word])/float(max)
		return word_tf

	def __iter__(self):
		return self.word_count.__iter__()
		

class DocumentCollection:
	"""
	A class that represents all indexed documents in scope.
	
	The collection is necessary because the idf needs calculates
	based upon the total number of *documents* that contain a term.
	
	word_count:	hash of each word and how many times that word appears in all documents.
	word_idf: hash of each word and its idf value
	documents: hash of the documents with the name of the document of the key
	maxterm: hash of the maximum occurence of any word in any document
	docfreq: the number of documents any given term exists in
	
	"""
	word_count = defaultdict(int)
	word_idf = defaultdict(float)
	documents = defaultdict(Document)
	maxterm = defaultdict(int) # (document_name, int)
	docfreq = defaultdict(int) # (word, int)
	
	def add_document(self, document):
		self.documents[document.name] = document
		self.maxterm[document.name] = max(document.word_count.values())
		
		for word in document.word_count:
			
			# Add the word to the total word count.
			self.word_count[word] += document.word_count[word]
			
			# Increment the total number of documents this word appears in.
			self.docfreq[word] += 1
			
		# Recalculate the idf hash.
		for word in self.word_count:
			# idf = log2[(total number of documents)/(number of documents containing the term)]
			idf = math.log(float(len(self.documents)) / float(self.docfreq[word]), 2)
			if idf == 0:
				self.word_idf[word] = .5
			else:
				self.word_idf[word] = idf
	
	
	# Gets a hash of the weights of the words in a given document.
	def get_weights(self, document):
		dict = defaultdict(int)
		for word in document.word_count:
			dict[word] = self.word_idf[word] * document.word_tf[word]
		return dict
		
	# Gets the length of either a document, or a query. A query does not use a tf value.
	def getlength(self, document):
		length = 0
		for word in document:
			if isinstance(document, Document):
				length += (self.word_idf[word] * document.word_tf[word])**2
			else:
				length += (self.word_idf[word])**2
		return math.sqrt(length)
		
	# Calculates dot-product of a query and a document.
	def _dot_product(self, query, document):
		total = 0
		words = set(query).intersection(set(document.word_count))
		for word in words:
			total += self.word_idf[word] * self.get_weights(document)[word]
		return total
	
	# Calculates the similarity between a query and a given document in the collection.
	def similarity(self, query, document):
		q = query.lower().split()
		return self._dot_product(q, document) / (self.getlength(q) * self.getlength(document))
		
	def __iter__(self):
		return self.documents.values().__iter__()






