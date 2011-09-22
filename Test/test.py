import sys
sys.path.append('../')
import ir
from collections import defaultdict

# Test data for homework 2.

documents = ('D1.txt','D2.txt','D3.txt')

Q = ' QUICK BROWN VEX ZEBRAS'.lower()


collection = ir.DocumentCollection()

d1 = ir.Document(documents[0])
d2 = ir.Document(documents[1])
d3 = ir.Document(documents[2])

collection.add_document(d1)
collection.add_document(d2)
collection.add_document(d3)


print 'D3 Weights - '
for word, weight in collection.get_weights(d3).items():
	print "{0}	{1}".format(word, weight)
	
print ''

similarities = defaultdict(float)

similarities[d1] =  collection.similarity(Q, d1)
similarities[d2] =  collection.similarity(Q, d2)
similarities[d3] =  collection.similarity(Q, d3)

print 'Similarities of Q on documents 1-3, ranked from best to worse.'
for (document, result) in sorted( similarities.items(), reverse=True):
	print "{0}	{1}".format(document.name, result)