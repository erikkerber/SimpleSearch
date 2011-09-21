from collections import defaultdict
# Test data for homework 2.

D1 = 'The quick brown fox jumps over a lazy brown dog'
D2 = 'Waltz, nymph, for quick jigs vex Bud'
D3 = 'How quickly daft jumping zebras vex'
Q = ' QUICK BROWN VEX ZEBRAS'

d1 = simplesearch.Document(D1)
d2 = simplesearch.Document(D2)
d3 = simplesearch.Document(D3)
q = Document(Q)
doc_collection = DocumentCollection({ d1, d2, d3 })

#for doc in doc_collection:
#	print '********'
#	for word in doc.document:
#		print word


print 'D3 Weights - '
for word, weight in doc_collection.get_weights(d3).items():
	print "{0}	{1}".format(word, weight)
	
print ''



print 'Q to D1', similarity(q, d1, doc_collection)
print 'Q to D2', similarity(q, d2, doc_collection)
print 'Q to D3', similarity(q, d3, doc_collection)