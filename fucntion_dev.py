#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:03:23 2020

@author: josh
"""


import praw
import pandas as pd
import datetime as dt

import disinfo.functions as di

reddit = praw.Reddit(client_id='RNGhJE66F0dfcg', 
                     client_secret='reMSAKkNv5daoHSRG3Cy15BhVw8', 
                     user_agent='cdc')



topics_dict = {  
                        "subreddit": [] 
                  }

topic_list = ["5g", "cats"] 

for topic in topic_list:
    
    cont_subreddit = reddit.subreddit("all").search(topic)
    
    for submission in cont_subreddit:
            topics_dict["subreddit"].append(submission.subreddit)
    


h = get_subreddit_data(reddit_object=reddit,  search_terms = ["cat", "Mouse"])



    
    
    
    
    