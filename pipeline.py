#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:03:23 2020

@author: josh

This pipeline takes an a topic or topics (any number equal or greater than 1) and returns the new comments for each subbredit where the topic was found 

"""

import disinfo as di
import praw

topics = ["cats", "dogs"]


reddit = praw.Reddit("reddit")        

subs_array = di.get_subreddit_names(reddit, topics)

database = di.get_subreddit_data(reddit, subs_array, comments=1)
