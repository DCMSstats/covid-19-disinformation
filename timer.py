#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:51:55 2020

@author: josh
"""

import pandas as pd
import pandas_gbq
import praw
import numpy as np
from prawcore import PrawcoreException
import datetime
import json
import disinfo as di
import time

start_time = time.perf_counter()


print("DEBUG- starting")

with open("gcp_config.json") as f:
    config = json.load(f)

project_id = config["project_id"]
table_sub  = config["table_sub"]
table_com  = config["table_com"]

comments_number = config["comments_number"]
topics_list = config["topics_list"]

client_id = config["client_id"]
client_secret = config["client_secret"]
user_agent =  config["user_agent"]

# init the praw instance
reddit = praw.Reddit(client_id = client_id, client_secret = client_secret,  user_agent = user_agent)

current_data = di.get_reddit(topics_list, comments_number, reddit_inst=reddit)

print("DEBUG - finished")

end_time = time.perf_counter()

print(f"time taken was {end_time - start_time:0.4f} seconds ")
