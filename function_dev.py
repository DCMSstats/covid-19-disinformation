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

com = database["comments"]

for i in com:
   print(i.body) 

h = print(com[0].body)

vars(h)

for comment in database.comments:
    print(comment.body)
    

  
    
def collect_comments(reddit_object, ids):
    """
    Given an array of ids for submissions collect comments from each submission

    Returns
    -------
    None.

    """
    
    topics_dict ={"comment_author":[], \
                  "id_from_thread":[], \
                  "comment_body":[], \
                  "comment_permalink":[],\
                  "comment_score":[]}
    
     
    for i in ids:
    
        submission = reddit.submission(id=i)
        submission.comments.replace_more(limit=None)
        
        for comment in submission.comments.list():
            topics_dict['comment_body'].append(comment.body)
            topics_dict['id_from_thread'].append(i)
            topics_dict['comment_author'].append(comment.author)
            topics_dict['comment_permalink'].append(comment.permalink)
            topics_dict['comment_score'].append(comment.score)
        
    topics_data = pd.DataFrame(topics_dict)
    return topics_data 
            
            
            
            
            




















