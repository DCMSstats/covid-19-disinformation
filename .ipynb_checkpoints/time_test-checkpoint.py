#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 11:16:17 2020

@author: josh
"""


import pandas as pd
import pandas_gbq
import praw
import numpy as np
from prawcore import PrawcoreException
import datetime
import time
import disinfo as di


start_time = time.perf_counter()

reddit = praw.Reddit(client_id='RNGhJE66F0dfcg',
                     client_secret='reMSAKkNv5daoHSRG3Cy15BhVw8',
                     user_agent='cdc')

comments_number = 100
topics_list = ["5g"]

current_data = di.get_reddit(topics_list, comments_number)

comment_data = di.get_comments(reddit, current_data.id)

end_time = time.perf_counter()
 
print(f"time taken was {end_time - start_time:0.4f} seconds ")
