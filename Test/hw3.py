import sys
sys.path.append('../')
import ir
import operator
from collections import defaultdict

# Test data for homework 3.

documents = ('D1.txt','D2.txt','D3.txt')

Q = ' QUICK BROWN VEX ZEBRAS'


collection = ir.DocumentCollection()

d1 = ir.Document(documents[0])
d2 = ir.Document(documents[1])
d3 = ir.Document(documents[2])

collection.add_document(d1)
collection.add_document(d2)
collection.add_document(d3)


print 'Document Weights - '
for doc in (d1, d2, d3):
	for word, weight in sorted(collection.get_weights(doc).iteritems(), key=operator.itemgetter(1)):
		print "{0}\t\t{1}\t\t{2}".format(word, weight, doc.name)
	
print ''

