import sys
import os
import csv

if __name__== "__main__" :

	with open(os.path.join('data', 'reducer.tsv'), 'w') as tsvfile:
	
		writer = csv.writer(tsvfile)
		pre_sg = ''
		sg_count = [0,0,0,0,0,0,0,0,0,0]
		sg_total_count = 0
		
		for line in sys.stdin:
		
			line = line.strip()
			if not line: continue
			
			tokens = line.split('\t')

			sg = tokens[0] + '\t' + tokens[1]
			index = 0

			if int(tokens[2]) < 0:
				index = int(tokens[2]) + 5
			else:
				index = int(tokens[2]) + 4

			count = int(tokens[3])

			if pre_sg == '':

				pre_sg = sg
				sg_count[index] += count
				sg_total_count = count
				continue

			if sg == pre_sg:

				sg_count[index] += count
				sg_total_count += count
				
			else:

				#writer.writerow([pre_sg + '\t' + str(count) + '\t' + '\t'.join(str(n) for n in sg_count)])
				print(pre_sg + '\t' + str(sg_total_count) + '\t' + '\t'.join(str(n) for n in sg_count))
				pre_sg = sg
				sg_count = [0,0,0,0,0,0,0,0,0,0]
				sg_count[index] += count
				sg_total_count = count
