import numpy as np
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import random
import pickle
from collections import Counter
from nltk.stem import WordNetLemmatizer
import re
import gensim.models
import ast
import json
import csv
from nltk.corpus import stopwords
from nltk.corpus import words
from collections import Counter
from urllib.parse import urlparse



lemmatizer = WordNetLemmatizer()

cachedStopWords = stopwords.words("english")


def num_of_words(line):
	words = line.split(' ')
	return len(words)


def avg_len_of_words(line):
	wordCount = num_of_words(line)
	length = 0
	words = line.split(' ');
	for word in words:
		length += len(word)
	return length/wordCount

def std_dev_of_word_length(line):
	word_length = []
	words = line.split(' ')
	for word in words:
		word_length.append(len(word))
	word_length = np.array(word_length)
	return np.std(word_length)

def digits_count(line):
	count = 0
	words = line.split(' ')
	for word in words:
		if(any(char.isdigit() for char in word)):
			count += 1
	return count

def num_stop_words(line):
	count = 0
	words = line.split(' ')
	for word in words:
		if word in stopwords.words('english'):
			count += 1
	return count

#print(num_stop_words("God i m going gr8 i also have 1 dog"))	
def num_invalid_words(line):   
	tweet_words = line.split(' ')
	invalid_words=0
	for word in tweet_words:
		if word not in words.words():
			invalid_words+=1
	return invalid_words
#print(num_invalid_words("Hi this is shilpa"))


def num_pos(line):
	tweet_words = line.split()
	tags = nltk.pos_tag(tweet_words)
	counts = Counter(tag for word,tag in tags)
	return len(counts)
#print(num_pos("hi my name is shilpa"))

def adding_features_with_tweets(fin,fout):
	with open(fin,'r') as finput:
		with open(fout,'w') as foutput:
			for line in finput:
				features = []
				label = line.split(':::')[0]
				tweet = line.split(':::')[1]
				tweet = tweet.lower()
				features.append(num_of_words(tweet))
				features.append(avg_len_of_words(tweet))
				features.append(std_dev_of_word_length(tweet))
				features.append(digits_count(tweet))
				features.append(num_stop_words(tweet))
				features.append(num_pos(tweet))
				features.append(num_invalid_words(tweet))
				foutput.write(label + ':::' + str(features) + ':::' + tweet)

#adding_features_with_tweets("train_tweets_small","train_tweets_small_features")


def clean_data(fin, fout):
	with open(fout, 'a') as foutput:
		with open(fin, 'r') as finput:
			for line in finput:
				text = line.split(':::')
				if(len(text) == 2):
					foutput.write(line)

		
#clean_data('test_tweets_p1','test_tweets_p1_clean')

def creat_lexicon(fin):
	lexicon = []
	with open(fin, 'r') as f:
		try:
			for line in f:
				text = line.split(':::')[1]
				content = ' '+text
				words = word_tokenize(content.lower())
				words = [lemmatizer.lemmatize(i) for i in words]
				for word in words:
					if word not in lexicon:
						lexicon.append(word)
				print(len(lexicon))
		except Exception as e:
			print(str(e))

	with open('lexicon.pickle','wb') as f:
		pickle.dump(lexicon,f)


#creat_lexicon("tweetsByCountry_onlyeng_clean")

def shuffle_data(fin,fout):
	with open(fout, 'a') as fout:
		lines = open(fin, 'r').readlines()
		random.shuffle(lines)
		for line in lines:
			fout.write(line)

#shuffle_data("tweetsByCountry_cleaned_stopwords_urls_shuffled_5","tweetsByCountry_cleaned_stopwords_urls_shuffled_6")



def print_lexicon_size():
	with open('lexicon.pickle','rb') as f:
		lexicon = pickle.load(f)
		print(lexicon)
		print(len(lexicon))

#print_lexicon_size()


def creat_country_array(fin):
	countries = []
	with open(fin, 'r') as f:
		try:
			for line in f:
				country = line.split(':::')[1]
				countries.append(country.lower().rstrip())
		except Exception as e:
			print(str(e))

	with open('countries.pickle','wb') as f:
		pickle.dump(countries,f)


#creat_country_array("countriesWithID")

#with open('countries.pickle','rb') as fcountry:
#	country = pickle.load(fcountry)
#	print(country)

def seperate_test_train(fin,ftrain,ftest):
	train_size = 30000
	test_size = 5000
	with open(fin,'rb') as fin:
		with open(ftrain,'wb') as ftrain:
			with open(ftest,'wb') as ftest:
				count =0
				for line in fin:
					if count < train_size:
						ftrain.write(line)
					else :
						break
					count += 1
#seperate_test_train('tweetsByCountry_cleaned_stopwords_urls_shuffled_script','tweetsByCountry_cleaned_stopwords_urls_shuffled_script_30000', 'test_tweets_features')

#eng_speaking_countries = ['Australia','Canada','Ireland','New Zealand','United Kingdom','United States']
#non_eng_speaking_countries = ['India','Pakistan','France','Ireland','Israel','Spain']
    
#[0 1] ---> english speaking countries
#[1 0] ---> non-english speaking countries

def retain_only_char_and_label(fin, fout):
	count = 0
	eng_speaking_countries = ['Australia','Canada','Ireland','United Kingdom','United States']
	non_eng_speaking_countries = ['India','Pakistan','Brazil','Germany','Japan']
	with open(fin,'r') as finput:
		with open(fout, 'a') as fout:
			for line in finput:
				if(len(line.split(':::')) >= 2):
					country = line.split(':::')[0]
					text = line.split(':::')[1]
					text = ' '.join([word for word in text.split() if not urlparse(word).scheme])
					text = re.sub('[^a-zA-Z0-9]',' ',text)
					text = re.sub(' +', ' ',text)
					text = ' '.join([word for word in text.split() if word not in cachedStopWords])
					if country in eng_speaking_countries:
						label = [0,1]
					elif country in non_eng_speaking_countries:
						label = [1,0]
					else:
						continue
					print(count)
					count += 1
					fout.write(str(label) + ':::' + text.rstrip() + '\n')


#retain_only_char_and_label("tweetsByCountry_onlyeng","tweetsByCountry_cleaned_stopwords_urls")

def creat_vec_lexicon(fin):
	lexicon = []
	with open(fin,'r') as finput:
		for line in finput:
			line = line.split(':::')[1]
			words = word_tokenize(line.lower())
			words = [lemmatizer.lemmatize(i) for i in words]
			lexicon.append(words)
	model = gensim.models.Word2Vec(lexicon, size=300, min_count=1)
	w2v = dict(zip(model.index2word, model.syn0))
	model.save('myw2vmodel_300')

#creat_vec_lexicon('tweetsByCountry_cleaned_stopwords_urls_shuffled_script_30000')


def create_vec_and_label_data(fin,foutput):
	model = gensim.models.Word2Vec.load('myw2vmodel_300')
	c = 0
	with open(foutput, 'a') as fout:
		with open(fin, 'r') as finput:
			for line in finput:
				c += 1
				print(c)
				label = line.split(':::')[0]
				line = line.split(':::')[1]
				pos = num_pos(line.lower())
				words = word_tokenize(line.lower())
				words = [lemmatizer.lemmatize(i) for i in words]
				sum = np.zeros(300,)
				count = 0
				for word in words:
					if word in model:
						count += 1
						sum += model[word]
				if count > 0:
					sum = sum/count
				if(eval(label)[0] == 0):
					class_tweet = 0
				else:
					class_tweet = 1
				fout.write(",".join(map(str,sum)) +','+ str(pos) +','+str(class_tweet) + '\n')	
create_vec_and_label_data('tweetsByCountry_cleaned_stopwords_urls_shuffled_script_30000','tweetsByCountry_cleaned_stopwords_urls_shuffled_script_30000_weka')




'''
with open('tiny_train_tweets_vecs') as f:
	for line in f:
		#label = ast.literal_eval(line.split(':::')[0])
		#tweet = line.split(':::')[1]
		#list = eval(label.rstrip())
		#print(list(eval(label)))
		print(eval(line.split(':::')[0]))
		'''

def tweets_to_csv(fin,fout):
	count = 0
	with open(fout, 'a') as foutput:
		with open(fin, 'r') as finput:
			writer = csv.writer(foutput)
			for line in finput:
				if(count <= 50000):
					label = line.split(':::')[0]
					tweet = line.split(':::')[1]
					if(eval(label)[0] == 0):
						cat = "eng"
					else:
						cat = "non-eng"
					row = [tweet, cat]
					writer.writerow(row)
					count += 1
				else:
					break

				

#tweets_to_csv('tweetsByCountry_labeled_cleaned_shuffled_3','tweetsByCountry_labeled_cleaned_shuffled_3.csv')

def removeStopWords(fin,fout):
	with open(fout, 'a') as foutput:
		with open(fin, 'r') as finput:
			for line in finput:
				label = line.split(':::')[0]
				tweet = line.split(':::')[1]
				tweet_words = tweet.split()
				for word in tweet_words:
					if word in stopwords.words('english'):						
							tweet_words.remove(word)
				foutput.write(str(label) + ':::' + str(tweet_words) + '\n')

#removeStopWords('tiny_tweets_cleaned_labeled','tiny_tweets_cleaned_labeled_noStopWords') 


def creat_eng_noneng_corpora(fin,feng,fnoneng):
	c=0
	with open(fin, 'r') as finput:
		with open(feng, 'a') as fouteng:
			with open(fnoneng, 'a') as foutneng:
				for line in finput:
					c += 1
					print(c)
					label = eval(line.split(':::')[0])
					tweet = line.split(':::')[1]
					if(label[0] == 0):
						foutneng.write(tweet)
					else:
						fouteng.write(tweet)

creat_eng_noneng_corpora('tweetsByCountry_cleaned_stopwords_urls_shuffled_script','eng_corpora','non-eng_corpora')

				