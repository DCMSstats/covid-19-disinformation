#!/usr/bin/env python3
import pandas as pd
import praw
from prawcore import PrawcoreException
import disinfo as di


def get_subreddit_names(reddit_object, search_terms, config):
    """
    Given a seach term returns all the subredits in which that term is mentioned

    Parameters
    ----------
    reddit_object : TYPE
        DESCRIPTION.
    search_terms : TYPE
        DESCRIPTION.

    Returns
    -------
    data : ndarrary object of numpy module
        DESCRIPTION.

    """
    reddit = reddit_object

    topics_dict = dict.fromkeys(config["get_subreddit_names_fields"], '')
    atts = topics_dict.keys()
    
    for term in search_terms:
    
        cont_subreddit = reddit.subreddit("all").search(term)
    
        for submission in cont_subreddit:
            for att in atts:
                try:
                    topics_dict[att].append(getattr(submission, att))
                except PrawcoreException as err:
                    topics_dict[att].append(err.args)
                except Exception as e:
                    topics_dict[att].append(e.__class__)
                    
    data = pd.DataFrame(topics_dict)
    data = data["subreddit"].apply(str).unique()

    return data


def get_subreddit_data(reddit_object, subs, config, comments= 10, sort='new'):
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

    topics_dict = dict.fromkeys(config["get_subreddit_data_fields"], [])

    atts = topics_dict.keys()
    
    sub_list = subs

    for sub in sub_list:

        print('Working on this sub right now: \n', sub)

        subreddit = reddit.subreddit(sub)

        submission_dict = {
            'new':subreddit.new, 
            'controversial':subreddit.controversial,
            'gilded':subreddit.gilded,
            'hot':subreddit.hot,
            'rising':subreddit.rising,
            'top':subreddit.top
        }

        cont_subreddit = submission_dict[sort](limit=comments)

        for submission in cont_subreddit:
            for att in atts:
                try:
                    topics_dict[att].append(getattr(submission, att))
                except PrawcoreException as err:
                    topics_dict[att].append(err.args)
                except Exception as e:
                    topics_dict[att].append(e.__class__)

    topics_data = pd.DataFrame(topics_dict)
    return topics_data


def get_redditor_data(redditors, connfig):
    """
    Given a array of redditors will return attrbutes of each redditor

    Parameters
    ----------
    def get_redditor_data : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """


    topics_dict = dict.fromkeys(config["get_redditor_data_fields"], [])

    atts = topics_dict.keys()
    
    for red in redditors:
            for att in atts:
                try:
                    topics_dict[att].append(getattr(red, att))
                except PrawcoreException as err:
                    topics_dict[att].append(err.args)
                except Exception as e:
                    topics_dict[att].append(e.__class__)

    topics_data = pd.DataFrame(topics_dict)
    return topics_data


def get_comments(reddit_object, ids):
    """
    Given an array of ids for submissions collect 
    comments from each submission

    Returns
    -------
    None.

    """
    reddit = reddit_object

    topics_dict = dict.fromkeys(config["get_comments_fields"], [])

    atts = topics_dict.keys()
    
    for i in ids:

        submission = reddit.submission(id=i)
        submission.comments.replace_more(limit=None)

        for comment in submission.comments.list():
            for att in atts:
                try:
                    topics_dict[att].append(getattr(comment, att))
                except PrawcoreException as err:
                    topics_dict[att].append(err.args)
                except Exception as e:
                    topics_dict[att].append(e.__class__)
                    
    topics_data = pd.DataFrame(topics_dict)
    return topics_data


def get_reddit(topics_list, comments_number, reddit_inst= "env"):
    """
    A wrapper for other disinfo functions to collect reddit data

    Parameters
    ----------
    reddit_inst : TYPE
        DESCRIPTION.
    topics_list : TYPE
        DESCRIPTION.
    comments_number : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    if reddit_inst == "env":
        reddit = praw.Reddit("reddit")
    else:
        reddit = reddit_inst

    subs_array = di.get_subreddit_names(reddit, topics_list)
    database = di.get_subreddit_data(
        reddit, subs_array, comments= comments_number, sort="new"
    )
    users = di.get_redditor_data(database.author)
    final_data = pd.concat([database, users], axis=1, join="outer")

    return final_data

def hash_usernames(df):
    """
    Given a dataframe this hashes rows under author columns

    Returns
    -------
    None.

    """    
    if 'author' in df:
        
        df.author = df.author.apply(lambda x:hash(x))

    if 'author' not in df:
    
        df.comment_author = df.comment_author.apply(lambda x:hash(x))        
