#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:18:23 2020

@author: josh
"""

import praw
import pandas as pd
import disinfo as di

comments_number = 5
topics_list = ["cats"]

reddit = praw.Reddit("reddit")

subs_array = di.get_subreddit_names(reddit, topics_list)

database = di.get_subreddit_data(reddit, subs_array, comments= comments_number, sort="new"  )

