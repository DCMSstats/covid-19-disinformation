#!/usr/bin/env python3
import pandas as pd

def get_subreddit_names(reddit_object, search_terms):
    
    reddit = reddit_object
    
    topics_dict = {  
                        "subreddit": [] 
                  }
    
    topic_list = search_terms
    
    for topic in topic_list:
    
        cont_subreddit = reddit.subreddit("all").search(topic)
        
        for submission in cont_subreddit:
                topics_dict["subreddit"].append(submission.subreddit)
        
    data = pd.DataFrame(topics_dict)
    
    data = data["subreddit"].apply(str).unique()
    
    return data
    