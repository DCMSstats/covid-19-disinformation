#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:03:23 2020

@author: josh
"""


import praw
import pandas as pd
import datetime as dt
import disinfo as di

reddit = praw.Reddit("reddit")        


def get_subreddit_names(reddit_object, search_terms):
    
    reddit = reddit_object
    
    topics_dict = {  
                        "subreddit": [] 
                  }
    
    topic_list = search_terms
    
    for topic in topic_list:
    
        cont_subreddit = reddit.subreddit("all").search(topic)
        
        for submission in cont_subreddit:
                topics_dict["subreddit"].append(submission.subreddit)
        
    data = pd.DataFrame(topics_dict)
    
    data = data["subreddit"].apply(str).unique()
    
    
    return data
    

p = get_subreddit_names(reddit, ["rstats"])
