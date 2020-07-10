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
current_data["created"] = current_data["created"].apply(di.convert_date)
current_data["backup_date"] = datetime.date.today()
current_data["backup_time"] = datetime.datetime.today().time()

print("DEBUG - data collected")

# find the earliest and latest date, used in the SQL query to check for duplicates

earliest_date = min(current_data["created"])
earliest_date_string =  earliest_date.strftime("%Y-%m-%d")

latest_date = max(current_data["created"])
latest_date_string =  latest_date.strftime("%Y-%m-%d")

sql = 'SELECT * FROM {0} WHERE backup_date > "{1}" AND backup_date < "{2}"'
SQL = sql.format(table_sub, earliest_date_string, latest_date_string)

# obtain data from the same period to check for duplciates
df = pandas_gbq.read_gbq(query=SQL, project_id=project_id)

# Remove duplcates
unique_data = di.data_to_add(newData=current_data, dataStore=df)

# Add data to bigquery
print("DEBUG-adding data to subbredit table")

pandas_gbq.to_gbq(unique_data, table_sub, project_id=project_id, if_exists="append")

# Get the comments data
print("DEBUG- collecting comment data")

comment_data = di.get_comments(reddit, unique_data.id)

# add the comment data to a seperate gbq table
pandas_gbq.to_gbq(comment_data, table_com, project_id=project_id, if_exists="append")

print("DEBUG - finished")

end_time = time.perf_counter()
 
print(f"time taken was {end_time - start_time:0.4f} seconds ")
