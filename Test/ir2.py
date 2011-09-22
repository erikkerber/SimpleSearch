from collections import defaultdict

# Debug flag: True=print intermediate data structures
DEBUG = True

# hardcoded (for simplicity) tuple of documents to index
documents = ('D1.txt','D2.txt','D3.txt')
maxterm = defaultdict(int)
docfreq = defaultdict(int)

index=defaultdict(int)	# dictionary key: (document, term), value: frequencies/weights
for document in documents:
	maxterm[document] = 0
	for line in open( document, 'r'):
		terms = line.split()
		for term in terms:
			if term != '':		# Ignore null results from split at start/end of line
				index[ ( document, term.lower() ) ] += 1
				if index[ (document, term.lower() ) ] > maxterm[document]:
					maxterm[document] = index[ (document, term.lower() ) ]
				


if DEBUG:
	print '\nRaw term count:'
	for ( document, term ) in sorted( index.keys() ):
		print document, term, index[ ( document, term ) ]
	print '\n Max term count'
	for document in sorted( maxterm.keys() ):
		print document, maxterm[document]