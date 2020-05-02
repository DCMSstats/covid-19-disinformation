#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 14:33:00 2020

@author: josh
"""

import praw
import pandas as pd
import datetime as dt

import disinfo.functions as di

reddit = praw.Reddit(client_id='RNGhJE66F0dfcg', 
                     client_secret='reMSAKkNv5daoHSRG3Cy15BhVw8', 
                     user_agent='cdc')


dict = {}

subs = ["rstats", "fuuny"]

for i in subs:
    dict[i] = reddit.subreddit(i)



subreddit2 = reddit.subreddit('rstats')
r_subreddit = subreddit2.new(limit=100)
    
reddit_data = {"title":[],
               "comments": [],
               "id": [],
               "score":[],
               "url": [],
               "created_utc": []}

for i in r_subreddit:
    reddit_data["title"].append(i.title)
    reddit_data["comments"].append(i.comments)
    reddit_data["id"].append(i.id)
    reddit_data["score"].append(i.score)
    reddit_data["url"].append(i.url)
    reddit_data["created_utc"].append(i.created_utc)
   

df = pd.DataFrame(reddit_data)

datetime_utc = df["created_utc"].apply(di.convert_date)

df = df.assign(datetime = datetime_utc)

# Earliest Date
print(min(datetime_utc))

# Latest Date
print(max(datetime_utc))


kay = di.get_subreddir_data(reddit, ["rstats"])



















