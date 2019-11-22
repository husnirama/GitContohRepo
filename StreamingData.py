"""
@author: Muhammad Rifky Y
"""

import os
import sys
import json
import tweepy
from time import time
from datetime import datetime,timedelta
try:os.chdir(os.path.dirname(__file__))
except:pass

consumer_key="4OF8QCNlOHzxemZKUFeuARDI4"
consumer_secret="p943ntn1HVLVpBSWBIaXqpsmjCjTmjDllikdW8icMOyi5y95sQ"
access_key="161673589-Mcf2LR8aXCL1pLjFgZK5ZhWEqvHrLvYLxnMV77p0"
access_secret="wmRbrC0SDhIuEMCvSt5rRNMplsts3Gj6B5k73QXXZmwOO"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True
    
class CustomStreamListener(tweepy.StreamListener):
    def on_connect(self):
        global detik,iterasi,namafolder
        if iterasi==0:
            print("Welcome {} (@{}), you are now connected to twitter server!".format(api.me().name,auth.get_username()))
        self.last_stream,self.namafile=datetime.now()+timedelta(seconds=detik),"{}/TwitStream_".format(namafolder)+str(datetime.now().replace(microsecond=0)).replace(":","")+".json"
        try:open(self.namafile,"w+").close()
        except FileNotFoundError: os.mkdir(self.namafile.split("/")[0])
        print("Streaming {} initiate at {}\n=====\n".format(iterasi+1,datetime.now().replace(microsecond=0)))
        print("Start streaming, please wait...")
        
    def from_creator(status):
        if hasattr(status, 'retweeted_status'):
            return False
        elif status.in_reply_to_status_id != None:
            return False
        elif status.in_reply_to_screen_name != None:
            return False
        elif status.in_reply_to_user_id != None:
            return False
        else:
            return True
    
    def on_status(self, status):
        global jmlh
        createdlocal=self.localtime(status.created_at)
        if createdlocal>=self.last_stream:
            print("\nTime's Up!\nTotal Records: {}".format(jmlh))
            print("You can open {} file saved in the same path as the script".format(self.namafile))
            return False
        with open(self.namafile, "a+") as tweet_log:
            tweet_log.write(json.dumps(status._json)+'\n')
            jmlh+=1
        print("\rData recorded @{1} (Total {0})".format(jmlh,createdlocal),end="")   
        
    def on_error(self, status_code):
        print('Encountered error with status code:', status_code, file=sys.stderr)
        timenow=datetime.fromtimestamp(time())
        if timenow>=self.last_stream:
            print("\nTime's Up!\nYou're no longer streaming\nTotal Records: {}".format(jmlh))
            print("You can open {} file saved in the same path as the script".format(self.namafile))
            return False
        print("Still streaming...")
        return True # Don't kill the stream

    def on_timeout(self):
        print('Timeout...', file=sys.stderr)
        timenow=datetime.fromtimestamp(time())
        if timenow>=self.last_stream:
            print("\nTime's Up!\nYou're no longer streaming\nTotal Records: {}".format(jmlh))
            print("You can open {} file saved in the same path as the script".format(self.namafile))            
            return False
        print("Still streaming...")
        return True # Don't kill the stream
    
    def localtime(self,utc_datetime):
        now_timestamp = time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset
  


sapi = tweepy.streaming.Stream(auth, CustomStreamListener())    
#sapi.filter(locations=[106.310621,-6.726237,107.224273,-6.041849])
namafolder="StreamingTest"
for i in range (3):
    jmlh,detik,iterasi=0,60,i
    #follows = ["69183155","135795460","17128975","23772644","255866913","47596019","104446991","124171593","219527452","177098799",
	#"108543358","55507370","57261519","18129942"]
    track="ini" #keyword
    region=[94.770705,-7.353750,140.976825,5.012150]
    sapi.filter(locations = region)
    #sapi.filter(track = track)
