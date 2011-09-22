import sys
sys.path.append('../')
import ir

# Test data for homework 2.



documents = ('D1.txt','D2.txt','D3.txt')

#D1 = 'The quick brown fox jumps over a lazy brown dog'
#D2 = 'Waltz, nymph, for quick jigs vex Bud'
#D3 = 'How quickly daft jumping zebras vex'
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


print 'Q to D1', ir.similarity(Q, d1, collection)
print 'Q to D2', ir.similarity(Q, d2, collection)
print 'Q to D3', ir.similarity(Q, d3, collection)