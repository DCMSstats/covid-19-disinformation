# -*- coding: utf-8 -*-
"""
Reddit exploatory script 

"""

# This script 

import praw
import pandas as pd
import datetime as dt

import disinfo.functions as di

reddit = praw.Reddit(client_id='RNGhJE66F0dfcg', 
                     client_secret='reMSAKkNv5daoHSRG3Cy15BhVw8', 
                     user_agent='cdc')


df = di.get_subreddir_data(reddit, ["rstats"],  limit= 20)

datetime_utc = df["created"].apply(di.convert_date)

df = df.assign(datetime = datetime_utc)ß

di.date_range(df["datetime"])

h = numpy.loadtxt("test.txt", dtype = 'str')


 