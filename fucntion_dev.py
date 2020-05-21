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

reddit = praw.Reddit("bot2")        


for submission in reddit.subreddit("rstats").hot(limit=10):
    print(submission.title)



    
    
    
    
    
