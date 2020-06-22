#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:18:23 2020

@author: josh
"""

import praw
import pandas as pd
import disinfo as di

comments_number = 1
topics_list = ["cats"]

reddit = praw.Reddit("reddit")

subs_array = di.get_subreddit_names(reddit, topics_list)

database = di.get_subreddit_data(reddit, subs_array, comments= comments_number, sort="new")

users = di.get_redditor_data(database.author)
            
final_data = pd.concat([database, users], axis=1, join="outer")
            
comment = di.get_comments(reddit_object = reddit , ids= database.id) 

for df in (database, final_data, comment):
    di.hash_usernames(df)
        