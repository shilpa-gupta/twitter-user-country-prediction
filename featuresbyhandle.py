#-*- coding: utf-8 -*-
import tweepy
from tweepy import Stream
import time
from tweepy import OAuthHandler
import json
from nltk.corpus import stopwords
from datetime import datetime, timedelta
import re
from urllib.parse import urlparse

ckey = 'affROYtP6LP4tmFQipA724cY2'
csecret = 'Tj40Q2iyZ70qeK2LEDd9A9Zb9li0RO7VBhgNmXVHHPxbqrwGvR'
atoken = '286622136-RKdeM1ZbAGPqf4VdD6IWowCPPFTl1Ey3cq1QyYOj'
asecret = 'BmExFibQ7JnH6aijSZ9VjQRyDjqY8jdZkWzY0EdJBzOLk'

auth = tweepy.AppAuthHandler(ckey, csecret)
#auth.set_access_token(atoken, asecret)

cachedStopWords = stopwords.words("english")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if(not api):
	print("can't Authenticate\n")
	sys.exit(-1)

def readUserObject(fin, fout):
	c = 0
	with open(fin, 'r') as finput:
		with open(fout, 'a') as foutput:
			for line in finput:
				user_data = []
				u_class = 1
				country = line.split(':::')[0]
				handle = line.split(':::')[1]
				try:
					user = api.get_user(screen_name=handle)
					if user:
						print(c)
						c += 1
						if int(user.statuses_count > 50):
							total_text = ""
							user_data.append(user.screen_name)
							user_data.append(user.followers_count)
							user_data.append(user.friends_count)
							user_data.append(user.statuses_count)
							user_data.append(user.id_str)
							user_data.append(user.favourites_count)
							user_data.append(country)
							created_at = user.created_at.isoformat()
							user_data.append(created_at)
							date_str=created_at[:10]
							user_data.append(user.statuses_count/(datetime.now().date()-datetime.strptime(date_str, "%Y-%m-%d").date()).days)
							try:
								rt_count=0
								tweets = api.user_timeline(screen_name = handle, count = 200, include_rts = False)
								tweet_count = 0
								user_tweets = []
								for tweet in tweets:
									tweet_count += 1							
									total_text = total_text + tweet.text
									tweet_text = ' '.join([word for word in tweet.text.split() if not urlparse(word).scheme])
									tweet_text = re.sub('[^a-zA-Z0-9]',' ',tweet_text)
									tweet_text = re.sub(' +', ' ',tweet_text)
									tweet_text = ' '.join([word for word in tweet_text.split() if word not in cachedStopWords])
									user_tweets.append(tweet_text)
									if tweet.retweet:
										rt_count+=1
								print(tweet_count)
								urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', total_text)
								user_data.append(len(urls))
								hash_tags = re.findall(r"#(\w+)", total_text)
								user_data.append(len(hash_tags))
								tags= re.findall(r"@(\w+)", total_text)
								user_data.append(len(tags))
								temp_text=total_text.encode('utf-16', 'surrogatepass').decode('utf-16')
								emojis=re.findall(u'[\U0001f600-\U0001f650]', temp_text)	
								user_data.append(len(emojis))
								user_data.append(rt_count)
								user_data.append(','.join(user_tweets))
								user_data.append(u_class)
								foutput.write(':::'.join(str(x) for x in user_data) + '\n')
							except tweepy.TweepError as e:
								print("some error : " + str(e))
								continue
				except tweepy.TweepError as e:
					print("some error : " + str(e))
					continue
readUserObject("usersByCountry/Japan_unq_users_8227", "featuresByUsers/Japan_8227")
# REMEMBER TO CHANGE THE CLASS ALL THE TIME