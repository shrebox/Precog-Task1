import tweepy
import sys
import jsonpickle
import os
import json
from pymongo import MongoClient
from collections import Counter
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt
import numpy as np
import re
import operator
from operator import itemgetter, attrgetter, methodcaller
from geopy.geocoders import Nominatim

client = MongoClient()
db = client.precog
collection = db.delhi_collection.find()

# # checking ids unique--------------------------------------
# idic = []
# count = 0
# for tweet in collection:
# 	if tweet['id'] not in idic:
# 		count+=1

# print count

# # checking the tweets of actually containing delhi keys----------------------------

# delhi_keys = ['delhi','new delhi','ncr','noida','faridabad','ghaziabad','ndls','gzb']
# txtcount=0
# for tweet in collection:
# 	for i in range(len(delhi_keys)):
# 		if delhi_keys[i] in tweet['text'].lower():
# 			txtcount+=1

# print txtcount

# top 10 hashtags----------------------------------------
hashdic = {}
count=0
for tweet in collection:
	for i in range(len(tweet['entities']['hashtags'])):
		if tweet['entities']['hashtags'][i]['text'] not in hashdic:
			hashdic[tweet['entities']['hashtags'][i]['text']] =1
		hashdic[tweet['entities']['hashtags'][i]['text']] +=1

count = 11
# check: sortedx = sorted(friendsdict.items(),key=operator.itemgetter(1))
for key, value in sorted(hashdic.iteritems(), key=lambda (k,v): (v,k),reverse=True):
	if count>0:
		print "%s: %s" % (key, value)
    	count-=1

# checking for extended entities---------------------------------------

extndic = {}
count=0
for tweet in collection:
	try:
		if tweet['extended_entities'] !=None:
			for i in range(len(tweet['extended_entities']['media'])):
				if tweet['extended_entities']['media'][i]['type'] not in extndic:
					extndic[tweet['extended_entities']['media'][i]['type']] = 1
				extndic[tweet['extended_entities']['media'][i]['type']] += 1
		if tweet['text'] !="":
			if 'text' not in extndic:
				extndic['text']=1
			extndic['text']+=1
	except:
		if tweet['text'] !="":
			if 'text' not in extndic:
				extndic['text']=1
			extndic['text']+=1

print extndic

# checking for the retweet status--------------------------------------------

retdic = {}
rtcount=0
oricount=0
for tweet in collection:
	try:
		if tweet['retweeted_status'] !=None:
			rtcount+=1
	except:
		oricount+=1

print "retweet count: " + str(rtcount)
print "original count: " + str(oricount)

# user location ----------------------------------------------------

delhi_keys = ['delhi','new delhi','ncr','noida','faridabad','ghaziabad','ndls','gzb']
ycount = ncount = 0
for tweet in collection:
	# if 'mumbai' in tweet['user']['location'].lower() or 'bombay' in tweet['user']['location'].lower():
	# 	print tweet['user']['location']
	# 	ycount+=1
	for i in range(len(delhi_keys)):
		if delhi_keys[i] in tweet['user']['location'].lower():
			print tweet['user']['location']
			ycount+=1
			break
	else:
		ncount+=1

print ycount,ncount

# geo check ----------------------------

geolocator = Nominatim()
xcor = []
ycor = []
geocount = 0
tzcount = 0
locount = 0
locdic = {}
pool=0
for tweet in collection:
	if tweet['geo'] != None:
		xcor.append(tweet['geo']['coordinates'][0])
		ycor.append(tweet['geo']['coordinates'][1])
		geocount+=1
	elif tweet['user']['time_zone'] != None:
		print tweet['user']['time_zone']
		try:
			if tweet['user']['time_zone'] not in locdic and tweet['user']['time_zone']!="":
				locdic[str(tweet['user']['time_zone'])] = 1
			locdic[str(tweet['user']['time_zone'])] += 1
		except:
			pool+=1
		tzcount+=1
	elif tweet['user']['location'] != None and tweet['user']['location']!="":
		print tweet['user']['location']
		try:
			if tweet['user']['location'] not in locdic:
				locdic[str(tweet['user']['location'])] = 1
			locdic[str(tweet['user']['location'])] += 1
		except:
			pool+=1
		locount+=1

print geocount, tzcount, locount

for i in range(len(xcor)):
	location = geolocator.reverse((xcor[i], ycor[i]))
	try:
		if location.address not in locdic:
			locdic[str(location.address)] = 1
		locdic[str(location.address)] += 1
	except:
		pool+=1

print locdic

# CDF favorite count of original tweets------------------------------------

favcount = []
for tweet in collection:
	try:
		if tweet['retweeted_status'] != None:
			favcount.append(tweet['retweeted_status']['favorite_count'])
	except:
		favcount.append(tweet['favorite_count'])

data_sorted = np.sort(favcount)

print data_sorted

p = 1. * np.arange(len(favcount)) / (len(favcount) - 1)

print len(p)

plt.title('Favorite counts CDF on original Tweets: Mumbai')
plt.plot(data_sorted, p)
plt.xlabel('Favorite Count')
plt.ylabel('CDF')
plt.show()

# network graph ---------------------------------------------

# 1. retweeted_status if ture => check the user id ==> id - retweeted_status[userid]
# 2. in reply to userid true ==> id - inreplytouserid
# 3. check entities['user_mentions'] if true ==> id - user_mentions id

import networkx as nx

G=nx.Graph()
networkdic = {}
origc = 0
for tweet in collection:
	try:
		if tweet['retweeted_status'] != None:
			G.add_edge(tweet['retweeted_status']['user']['id'],tweet['user']['id'])
	except:
		origc+=1

	if tweet['in_reply_to_user_id'] != None:
		G.add_edge(tweet['in_reply_to_user_id'],tweet['user']['id'])

	for i in range(len(tweet['entities']['user_mentions'])):
		G.add_edge(tweet['entities']['user_mentions'][i]['id'],tweet['user']['id'])

	# try:
	# 	if tweet['retweeted_status'] != None:
	# 		if tweet['retweeted_status']['user']['id'] not in networkdic:
	# 			networkdic[tweet['retweeted_status']['user']['id']] = [tweet['user']['id']]
	# 		else:
	# 			networkdic[tweet['retweeted_status']['user']['id']].append(tweet['user']['id'])
	# 		# if tweet['user']['id'] not in networkdic:
	# 		# 	networkdic[tweet['user']['id']] = [tweet['retweeted_status']['user']['id']]
	# 		# else:
	# 		# 	networkdic[tweet['user']['id']].append(tweet['retweeted_status']['user']['id'])
	# except:
	# 	origc+=1

	# if tweet['in_reply_to_user_id'] != None:
	# 	if tweet['in_reply_to_user_id'] not in networkdic:
	# 		networkdic[tweet['in_reply_to_user_id']] = [tweet['user']['id']]
	# 	else:
	# 		networkdic[tweet['in_reply_to_user_id']].append(tweet['user']['id'])
	# 	# if tweet['user']['id'] not in networkdic:
	# 	# 	networkdic[tweet['user']['id']] = [tweet['in_reply_to_user_id']]
	# 	# else:
	# 	# 	networkdic[tweet['user']['id']].append(tweet['in_reply_to_user_id'])

	# for i in range(len(tweet['entities']['user_mentions'])):
	# 	if tweet['entities']['user_mentions'][i]['id'] not in networkdic:
	# 		networkdic[tweet['entities']['user_mentions'][i]['id']] = [tweet['user']['id']]
	# 	else:
	# 		networkdic[tweet['entities']['user_mentions'][i]['id']].append(tweet['user']['id'])
	# 	# if tweet['user']['id'] not in networkdic:
	# 	# 	networkdic[tweet['user']['id']] = [tweet['entities']['user_mentions'][i]['id']]
	# 	# else:
	# 	# 	networkdic[tweet['user']['id']].append(tweet['entities']['user_mentions'][i]['id'])


nx.draw(G,with_labels=False)
plt.title("Delhi Network")
plt.savefig('delhi_network.eps', format='eps', dpi=1000)
plt.show()

# for key,value in networkdic.iteritems():
# 	print key, value[0]

# print len(networkdic)

		