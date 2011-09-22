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
			print "Can't read ", name
			
		self.name = name	
			
		# Split the document into a list of words
		self.document = re.split('\W+', str.lower(doc))
		
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
	
	word_count:	hash of each word and how many times that word appears.
	
	"""
	word_count = defaultdict(int)
	word_documentcount = defaultdict(int)
	word_idf = defaultdict(float)
	document_length = defaultdict(float)
	documents = defaultdict(Document)
	maxterm = defaultdict(int)

	
	def add_document(self, document):
		self.documents[document.name] = document
		self.maxterm[document.name] = max(document.word_count.values())
		
		for word in document.word_count:
			
			# Add the word to the total word count.
			self.word_count[word] += document.word_count[word]
			
			# Increment the total number of documents this word appears in.
			self.word_documentcount[word] += 1
			
		# Recalculate the idf hash.
		for word in self.word_count:
			# idf = log2[(total number of documents)/(number of documents containing the term)]
			self.word_idf[word] = math.log(float(len(self.documents)) / float(self.word_documentcount[word]), 2)
	
	
	def get_weights(self, document):
		dict = defaultdict(int)
		for word in document.word_count:
			dict[word] = self.word_idf[word] * document.word_tf[word]
		return dict
		
	def getlength(self, document):
		length = 0
		for word in document:
			if isinstance(document, Document):
				length += (self.word_idf[word] * document.word_tf[word])**2
			else:
				length += (self.word_idf[word])**2
		return math.sqrt(length)
		
		
def similarity(query, document, doc_collection):
	q = query.split()
	return dot_product(q, document, doc_collection) / (doc_collection.getlength(q) * doc_collection.getlength(document))

def dot_product(query, document, document_collection):
	total = 0
	words = set(query).intersection(set(document.word_count))
	for word in words:
		total += document_collection.word_idf[word] * document_collection.get_weights(document)[word]
	return total



