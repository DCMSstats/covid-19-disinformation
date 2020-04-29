# -*- coding: utf-8 -*-
"""
Reddit exploatory script 

"""

import praw
import pandas as pd

reddit = praw.Reddit(client_id='RNGhJE66F0dfcg', 
                     client_secret='reMSAKkNv5daoHSRG3Cy15BhVw8', 
                     user_agent='cdc')

subreddit2 = reddit.subreddit('rstats')
r_subreddit = subreddit2.new(limit=1000)
    
reddit_data = {"title":[],
               "comments": [],
               "id": [],
               "score":[],
               "url": []}

for i in r_subreddit:
    reddit_data["title"].append(i.title)
    reddit_data["comments"].append(i.comments)
    reddit_data["id"].append(i.id)
    reddit_data["score"].append(i.score)
    reddit_data["url"].append(i.url)
   

df = pd.DataFrame(reddit_data)
