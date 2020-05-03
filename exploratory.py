# -*- coding: utf-8 -*-
"""
Reddit exploatory script 

"""

import praw
import pandas as pd
import datetime as dt

import disinfo.functions as di

reddit = praw.Reddit(client_id='RNGhJE66F0dfcg', 
                     client_secret='reMSAKkNv5daoHSRG3Cy15BhVw8', 
                     user_agent='cdc')


df = di.get_subreddir_data(reddit, ["rstats"])


datetime_utc = df["created_utc"].apply(di.convert_date)

df = df.assign(datetime = datetime_utc)

k = di.date_range(df["datetime"])


