#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:18:23 2020

@author: josh
"""

import praw
import pandas as pd
import disinfo as di
reddit = praw.Reddit("reddit")

reddit_data = di.get_reddit(["cats"], 5)
            
comment = di.get_comments( reddit_object = reddit , ids= reddit_data.id) 



