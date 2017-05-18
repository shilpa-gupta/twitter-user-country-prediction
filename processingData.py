import random
import gensim.models
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def mergeAllCountries(fin , fout):
	with open(fin,'r') as finput:
		with open(fout,'a') as foutput:
			for line in finput:
				foutput.write(line)

#mergeAllCountries('non-eng_merged','English_Merged')

def shuffle_data(fin,fout):
	with open(fout, 'a') as fout:
		lines = open(fin, 'r').readlines()
		random.shuffle(lines)
		for line in lines:
			fout.write(line)

#shuffle_data('English_Merged','Total_shuffled')

def creat_vec_lexicon(fin):
	lexicon = []
	c=0
	with open(fin,'r') as finput:
		for line in finput:
			c+=1
			print(c)
			line = line.split(':::')[14]			
			words = word_tokenize(line.lower())
			words = [lemmatizer.lemmatize(i) for i in words]
			lexicon.append(words)
	model = gensim.models.Word2Vec(lexicon, size=100, min_count=1,sg=0)
	w2v = dict(zip(model.index2word, model.syn0))
	model.save('myw2vmodel')

#creat_vec_lexicon('Total_shuffled')

def create_vec_and_label_data(fin,foutput):
	model = gensim.models.Word2Vec.load('myw2vmodel')
	with open(foutput, 'a') as fout:
		with open(fin, 'r') as finput:
			c=0
			for line in finput:
				user_data = []
				c+=1
				print(c)				
				features=line.split(':::')
				user_data.append(features[2])
				user_data.append(features[1])
				user_data.append(features[3])
				user_data.append(features[8])
				user_data.append(features[9])
				user_data.append(features[10])
				user_data.append(features[11])
				user_data.append(features[12])
				user_data.append(features[13])
				line = features[14]
				words = word_tokenize(line.lower())
				words = [lemmatizer.lemmatize(i) for i in words]
				sum = np.zeros(100,)
				count=0				
				for word in words:
					if word in model:
						count+=1
						sum += model[word]						
				
				if count>0 :
					sum=sum/count
				else:
					sum=sum/1
				user_data.append(",".join(map(str,sum)))
				user_data.append(features[15].rstrip())
				print(','.join(user_data) +'\n')
				#fout.write(','.join(user_data) +'\n')	
#create_vec_and_label_data('Total_shuffled','Total_Data_weka')

def removing_rt_count(fin,fout):
	with open(foutput, 'a') as fout:
		with open(fin, 'r') as finput:	
			for line in finput:
				user_data = []
				features=line.split(',')
				new_features=[x.rstrip() for x in features]
				print(new_features)
				new_features.pop(8)
				foutput.write(','.join(new_features)+'\n')
	

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
#extract_sub_tweets('total_data','sub_data_unprocessed/data150')