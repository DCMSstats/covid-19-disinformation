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
    


def get_subreddit_data(reddit_object, subs, comments = 10):
    """
        Get Subreddit data
        
        Parameters
        ----------
        reddit_object : stuffs
         
        Returns
        -------
        Pandas Dataframe
        """
   
    reddit = reddit_object
    
    topics_dict = {     "title":[], \
                        "score":[], \
                        "id":[], "url":[], \
                        "comms_num": [], \
                        "created": [], \
                        "body":[], \
                        "subreddit": [] 
                  }
        
    sub_list = subs
    
    for sub in sub_list:
    
        print('Working on this sub right now: \n', sub)
    
        subreddit = reddit.subreddit(sub)
    
        cont_subreddit = subreddit.new(limit=comments)
    
        for submission in cont_subreddit:
            topics_dict["title"].append(submission.title)
            topics_dict["score"].append(submission.score)
            topics_dict["id"].append(submission.id)
            topics_dict["url"].append(submission.url)
            topics_dict["comms_num"].append(submission.num_comments)
            topics_dict["created"].append(submission.created)
            topics_dict["body"].append(submission.selftext)
            topics_dict["subreddit"].append(submission.subreddit)
            
    topics_data = pd.DataFrame(topics_dict)
    return topics_data    
    