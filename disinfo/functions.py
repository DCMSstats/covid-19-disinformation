#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions
"""

import datetime as dt
import pandas as pd
import yaml

def convert_date(x):
   return dt.datetime.fromtimestamp(x)

def hello(name):
    print("Hello " + name)
    return

    
def date_range(x):
    early = min(x)
    late = max(x)
    return early, late, print(f"The latest date is is {late} and the earliest date is {early}")

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
    
    return data
    

def load_config(config_file = "config.yaml"):
    
    config_yml = open(config_file)
    config = yaml.load(config_yml)
    return config
