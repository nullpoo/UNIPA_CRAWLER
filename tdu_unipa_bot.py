#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        tdu_unipa_bot
#
# Author:      nullpoo
#
# Created:     08/08/2012
#-------------------------------------------------------------------------------

import tweepy
import urllib, urllib2
import unicodedata
import json
import datetime
import random

def GetRequest(uri):
    req = urllib2.Request(uri)
    opener = urllib2.build_opener()
    res = opener.open(req)
    result = res.read()
    return result

consumer_key = 	'[CONSUMER_KEY]'
consumer_secret = '[CONSUMER_SECRET]'
access_key = '[ACCESS_KEY]'
access_secret = '[ACCESS_SECRET]'

# create OAuth handler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# set access token to OAuth handler
auth.set_access_token(access_key, access_secret)
# create API
api = tweepy.API(auth_handler=auth)

#日付生成
today = datetime.datetime.now().strftime('%Y-%m-%d')
print today
#JSONの取得
uri = "http://nullserver.jp/nullpo/sqlout.py?fdate="+today+"&tdate="+today
strjson = GetRequest(uri)
dic = json.loads(strjson)
rand = random.randrange(0,100)
for item in dic:
    print str(item[u'title'].encode('utf-8'))
    api.update_status(item[u'title']+","+str(rand).encode('utf-8'))
