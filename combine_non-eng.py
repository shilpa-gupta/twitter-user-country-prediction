def combine_non_eng(fin,fout):
	with open(fin, 'r') as finput:
		with open(fout,'a') as foutput:
			for line in finput:
				foutput.write(line)

#combine_non_eng("../final_data/US_21531",'total_data')

def extract_sub_tweets(fin,fout):
		c = 0
		var = 150
		with open(fin, 'r') as finput:
			with open(fout, 'a') as foutput:
				for line in finput:
					line = line.split(':::');
					u_class = line.pop(-1).rstrip()
					text = line.pop(-1)
					text = text.split(',')
					if(len(text) > var):
						text = ','.join(text[:var])
						line.append(text)
						line.append(u_class)
						print(c)
						c += 1
						foutput.write(':::'.join(map(str,line)) + '\n')
extract_sub_tweets('total_data','sub_data_unprocessed/data150')