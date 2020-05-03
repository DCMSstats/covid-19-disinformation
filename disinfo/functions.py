#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions
"""

import datetime as dt
import pandas as pd

def convert_date(x):
   return dt.datetime.fromtimestamp(x)

def hello(name):
    print("Hello " + name)
    return

def get_subreddir_data(reddit_object, subs, limit = 10):
    
    reddit = reddit_object
    
    topics_dict = {     "title":[], \
                        "score":[], \
                        "id":[], "url":[], \
                        "comms_num": [], \
                        "created": [], \
                        "body":[], \
                        "subreddit": [] 
                  }
        
    sub_list = subs
    
    for sub in sub_list:
    
        print('Working on this sub right now: \n', sub)
    
        subreddit = reddit.subreddit(sub)
    
        cont_subreddit = subreddit.new(limit=limit)
    
        for submission in cont_subreddit:
            topics_dict["title"].append(submission.title)
            topics_dict["score"].append(submission.score)
            topics_dict["id"].append(submission.id)
            topics_dict["url"].append(submission.url)
            topics_dict["comms_num"].append(submission.num_comments)
            topics_dict["created"].append(submission.created)
            topics_dict["body"].append(submission.selftext)
            topics_dict["subreddit"].append(submission.subreddit)
            
    topics_data = pd.DataFrame(topics_dict)
    return topics_data    
    
def date_range(x):
    early = min(x)
    late = max(x)
    return early, late, print(f"The latest date is is {late} and the earliest date is {early}")



