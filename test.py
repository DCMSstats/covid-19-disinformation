#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 14:33:00 2020

@author: josh
"""

import praw
import pandas as pd
import datetime as dt

import disinfo.functions as di

reddit = praw.Reddit(client_id='RNGhJE66F0dfcg', 
                     client_secret='reMSAKkNv5daoHSRG3Cy15BhVw8', 
                     user_agent='cdc')


dict = {}

subs = ["rstats", "fuuny"]



kay = di.get_subreddir_data(reddit, ["rstats"])



















