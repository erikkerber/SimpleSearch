from collections import defaultdict
import math

D1 = 'The quick brown fox jumps over a lazy brown dog'
D2 = 'Waltz, nymph, for quick jigs vex Bud'
D3 = 'How quickly daft jumping zebras vex'
Q = ' QUICK BROWN VEX ZEBRAS'

class Document:
	
	"""
	Object represeting a document or query.
	"""
	document = None
	word_count = None
	word_tf = None
	term_weights = None
	length = 0
	highest = 0
	
	def __init__(self, doc):
		self.document = str.lower(doc).split()
		self.word_count, self.highest= self._tokenize(self.document)
		self.word_tf = self._get_tf()
		self.term_weights = self._get_term_weights()
		self.length = self._get_length()
		
		
	def _tokenize(self, document):
		word_count = defaultdict(int)
		highest = 0
		for word in document:
			word_count[word] += 1
			if word_count[word] > highest:
				highest = word_count[word]
		return word_count, highest
		
	# tf= (term count in a document)/(largest term count in a document)
	def _get_tf(self):
		word_tf = defaultdict(float)
		for word in self.word_count:
			word_tf[word] = float(self.word_count[word])/float(self.highest)
		return word_tf
		
	# Brad says we are only using idf's for now.
	def _get_term_weights(self):
		return self.word_tf.values()

	def _get_length(self):
		length = 0
		for term in self.term_weights:
			length += term**2
		return math.sqrt(length)

class DocumentCollection:
	"""
	A class that represents all indexed documents in scope.
	
	The collection is necessary because the idf needs calculates
	based upon the total number of documents that contain a term.
	
	"""
	word_count = defaultdict(int)
	word_documentcount = defaultdict(int)
	word_idf = defaultdict(float)
	document_length = defaultdict(float)
	documents = None
	
	def __init__(self, documents):
		self.documents = documents
		for doc in documents:
			for word in doc.word_count:
				self.word_count[word] += doc.word_count[word]
				self.word_documentcount[word] += 1
		self.word_idf = self._get_idf()
	
	# idf = log2[(total number of documents)/(number of documents containing the term)]
	def _get_idf(self):
		word_idf = defaultdict(float)
		for word in self.word_count:
			word_idf[word] = math.log(float(len(self.documents)) / float(self.word_documentcount[word]), 2)
		return word_idf
		
	def get_weights(self, query):
		dict = defaultdict(int)
		for word in query.word_count:
			dict[word] = self.word_idf[word] * query.word_tf[word]
		return dict
		
	def getlength(self, query):
		length = 0
		for word in query.word_count:
			#print (self.word_idf[word] * query.word_tf[word]), word
			length += (self.word_idf[word] * query.word_tf[word])**2
		return math.sqrt(length)
		
def similarity(d1, d2, doc_collection):
	return dot_product(d1, d2, doc_collection) / (doc_collection.getlength(d1) * doc_collection.getlength(d2))

def dot_product(d1, d2, document_collection):
	total = 0
	words = set(d1.word_count).union(set(d2.word_count))
	for word in words:
		total += document_collection.get_weights(d1)[word] * document_collection.get_weights(d2)[word]
	return total


# Test data for homework 2.

d1 = Document(D1)
d2 = Document(D2)
d3 = Document(D3)
q = Document(Q)
doc_collection = DocumentCollection({ d1, d2, d3 })

print doc_collection.get_weights(d3)
print similarity(d2, d3, doc_collection)
#print similarity(q, d1, doc_collection)

#print a.word_idf
