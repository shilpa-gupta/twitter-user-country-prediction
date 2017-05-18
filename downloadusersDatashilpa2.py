import tweepy
from tweepy import Stream
import time
from tweepy import OAuthHandler
import json


'''
ckey = 'k20L6wCHk1PSzHQEjaSPCTHeR'
csecret = 'CDyt9N6IzS81l1pJGzYAMYshWr6FB86xDw2bxaMDM3KklWySN'
atoken = '801230718349275136-toEZGOK2EOP5BJT7vZRYW38MGr7XNK'
asecret = 'y8eitvtSMAnjplqs1oabt331kwArNlQmEozEb0IwomvtH'
'''
ckey = 'aBOEqrijUZvgfCpF1RAYMV1zr'
csecret = '5Dw7Bw1vWXK5GezykPbZreZ8ogev0If3Z0aOdUeIFMDP7zvMZu'
atoken = '286622136-qOW2VsqIhN1xOrTJtwDCKjIwUwFmaIv4yh9o0Mx'
asecret = 'TluPFloabfxF0Blfh3gCgREoc3SEU66BK1lZdQi2rIjOJ'
auth = tweepy.AppAuthHandler(ckey, csecret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if(not api):
	print("can't Authenticate\n")
	sys.exit(-1)

def readUserObject(fin, fout):
	c = 0
	with open(fin, 'r') as finput:
		with open(fout, 'a') as foutput:
			for line in finput:
				user_json = {}
				country = 'Germany'
				handle = line.rstrip()
				try:
					user = api.get_user(screen_name=handle)
					if user:
						print(c)
						c += 1
						user_json['screen_name'] = user.screen_name
						user_json['followers_count'] = user.followers_count
						user_json['friends_count'] = user.friends_count
						user_json['statuses_count'] = user.statuses_count
						user_json['id_str'] = user.id_str
						user_json['favourites_count'] = user.favourites_count
						user_json['country'] = country
						user_json['class'] = 1
						user_json['created_at'] = user.created_at.isoformat()
					foutput.write(json.dumps(user_json))
				except tweepy.TweepError as e:
					print("some error user not found")
					continue

readUserObject("Germany_unq_users", "Germany_unq_users_features")

def get_user_ids(fin,fout):
	source_list=[]
	with open(fin,'r') as finput:
		with open(fout,'w') as foutput:
			for line in finput:
				label = line.split(':::')[0]
				id = line.split(':::')[1]
				source_list.append(id)
			unique_ids=list(set(source_list))
			for id in unique_ids:
				foutput.write(str(id))
#get_user_ids('twitter_user_ids_with_country_India','india_unq_users')