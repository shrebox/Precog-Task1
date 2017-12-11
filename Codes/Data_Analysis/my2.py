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


		