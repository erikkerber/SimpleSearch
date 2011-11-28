import sys
sys.path.append('../')
import ir
import operator
from collections import defaultdict


# Create ir3.pl based on ir2.pl (due on 10/20)
# * Repeatedly prompt the user for a query (if they enter 'q', then quit)
# * Find the terms in the query, and calculate the appropriate weight for each query term
# * Calculate the similarity for each query/document pair
# * List the documents in order of decreasing similarity to the query, along with their similarity value
# * Your results for "quick brown vex zebras" should be
# * D1.txt 0.42, D3.txt 0.33, D2.txt 0.08
# * Make sure that querying "quick brown vex zebras" a 2nd time gives the same result
# * What is the result for the query "quick brown vex lion"? (Note: If the denominator of IDF is 0, like for "lion", set the denominator to 0.5)

documents = ('D1.txt','D2.txt','D3.txt')

Q = ' QUICK BROWN VEX ZEBRAS'


collection = ir.DocumentCollection()

d1 = ir.Document(documents[0])
d2 = ir.Document(documents[1])
d3 = ir.Document(documents[2])

collection.add_document(d1)
collection.add_document(d2)
collection.add_document(d3)

while True:
	query = raw_input("Enter a query: ")
	if query == 'q':
		break;
	else:
		Q = ir.Document(query)
		# * Find the terms in the query, and calculate the appropriate weight for each query term
		#for key, value in Q.word_tf.items():
		#	print key, value

		#print '____________________'

		# * Calculate the similarity for each query/document pair
		similarities = defaultdict(float)
		for doc in collection:
			similarities[doc] = collection.similarity(Q.source, doc)
		
		for doc in sorted(similarities.items()):
			print doc[0].name, doc[1]
		#collection.similarity(query, d1)
		print "continuing"
		
	
#print 'Document Weights - '
#for doc in (d1, d2, d3):
#	for word, weight in sorted(collection.get_weights(doc).iteritems(), key=operator.itemgetter(1)):
#		print "{0}\t\t{1}\t\t{2}".format(word, weight, doc.name)
#	
#print ''

