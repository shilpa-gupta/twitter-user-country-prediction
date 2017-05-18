import tweepy
from tweepy import Stream
import time
from tweepy import OAuthHandler

ckey = 'affROYtP6LP4tmFQipA724cY2'
csecret = 'Tj40Q2iyZ70qeK2LEDd9A9Zb9li0RO7VBhgNmXVHHPxbqrwGvR'
atoken = '286622136-RKdeM1ZbAGPqf4VdD6IWowCPPFTl1Ey3cq1QyYOj'
asecret = 'BmExFibQ7JnH6aijSZ9VjQRyDjqY8jdZkWzY0EdJBzOLk'

auth = tweepy.AppAuthHandler(ckey, csecret)
#auth.set_access_token(atoken, asecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if(not api):
	print("can't Authenticate")
	sys.exit(-1)

def extractPlaceIDs(infile,outfile):
	name_id_file = open(outfile,"a")
	with open(infile,"r") as f:
		for line in f:
			places = api.geo_search(query=line, granularity="country")
			place_id = places[0].id
			name_id_file.write(place_id + ':::' + line)



#extractPlaceIDs("countries.py","countriesWithID")

def readTweetByCountry(countryIdFile, TweetFile):
	maxTweets = 10000
	tweetsPerQry = 100
	sinceId = None
	max_id = -1
	tweetCount = 0
	with open (TweetFile,"a") as tweet_file:
		with open(countryIdFile, "r") as file:
			for line in file:
				tweetCount = 0
				id = line.split(':::')[0]
				country = line.split(':::')[1]
				while(tweetCount < maxTweets):
					try:
						if(max_id <= 0):
							if(not sinceId):
								new_tweets = api.search(q="place:%s & lang:en" % id, count=tweetsPerQry)
							else:
								new_tweets = api.search(q="place:%s & lang:en" % id, count=tweetsPerQry, since_id=sinceId)
						else:
							if(not sinceId):
								new_tweets = api.search(q="place:%s & lang:en" % id, count=tweetsPerQry, max_id = str(max_id-1))
							else:
								new_tweets = api.search(q="place:%s & lang:en" % id, count=tweetsPerQry, max_id=str(max_id-1), since_id=sinceId)

						if not new_tweets:
							print("No More tweets found")
							break
						for tweet in new_tweets:
							print("*****"+country+"*******")
							tweet_file.write(country.rstrip()+":::"+tweet.text+'\n')
						tweetCount += len(new_tweets)
						print("Downloaded {0} tweets".format(tweetCount))
						max_id = new_tweets[-1].id
					except tweepy.TweepError as e:
						print("some error : " + str(e))
						break 				


readTweetByCountry("currentCountryID","tweetsByCountry_onlyeng")
