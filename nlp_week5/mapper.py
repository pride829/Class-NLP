import sys
import os
import csv
import string

def dict_add(d: dict, s: str):
	if not s in d:
		d[s] = 1
	else:
		d[s] += 1
	return

def _map(line: str, sg_count: dict):

	line = line.lower()
	line = line.translate(str.maketrans(string.punctuation + '–',
                              ''.join(' ' for c in string.punctuation + '–')))
        
	tokens = line.split()
        
        
	for i in range(0, len(tokens)):
		for j in range(-5, 6):
			if j == 0 or not i+j in range(0, len(tokens)):
				continue
			dict_add(sg_count, '\t'.join([tokens[i], tokens[i+j], str(j)]))

if __name__== "__main__" :

	sg_count = {}
	for line in sys.stdin:
		_map(line, sg_count)
	
	#with open(os.path.join('data', 'mapper.tsv'), 'w') as tsvfile:
	#	writer = csv.writer(tsvfile)
	#	for d in sg_count:
	#		writer.writerow([d + '\t' + str(sg_count[d])])
	for d in sg_count:
		print(d + '\t' + str(sg_count[d]))
