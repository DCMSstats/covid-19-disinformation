# A test to collect a large amount of subbredits

import praw
import pandas as pd
import datetime as dt
import sys
import numpy as np

import disinfo.functions as di

reddit = praw.Reddit("reddit")


def get_subreddits():

    df = di.get_subreddir_data(reddit, ["all"],  limit= 1000)
    un = df["subreddit"].unique()

    sys.stdout=open("test2.txt","w")
    for i in un:
        print(i)

    sys.stdout.close()
    subreddits = np.loadtxt("test2.txt", dtype = 'str')
    
    return(subreddits)


hit = get_subreddits()

df = di.get_subreddir_data(reddit, ["all"],  limit= 1000)
 
print("test")