#!/usr/bin/env python3
import pandas as pd
import praw
from prawcore import PrawcoreException
import disinfo as di

def get_subreddit_names(reddit_object, search_terms):

    reddit = reddit_object

    topics_dict = {
                        "subreddit": []
                  }

    topic_list = search_terms

    for topic in topic_list:

        cont_subreddit = reddit.subreddit("all").search(topic)

        for submission in cont_subreddit:
            try:
                topics_dict["subreddit"].append(submission.subreddit)
            except PrawcoreException as err:
                topics_dict["subreddit"].append(err.args)
            except Exception as e:
                topics_dict["subreddit"].append(e.__class__)

    data = pd.DataFrame(topics_dict)

    data = data["subreddit"].apply(str).unique()

    return data


def get_subreddit_data(reddit_object, subs, comments= 10, sort='new'):
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
                        "subreddit": [],
                        "author": [],
                        "comments": []
                  }

    sub_list = subs

    for sub in sub_list:

        print('Working on this sub right now: \n', sub)

        subreddit = reddit.subreddit(sub)

        submission_dict ={'new':subreddit.new, \
                          'controversial':subreddit.controversial,\
                          'gilded':subreddit.gilded,\
                          'hot':subreddit.hot,\
                          'rising':subreddit.rising,\
                          'top':subreddit.top }


        cont_subreddit = submission_dict[sort](limit=comments)

        for submission in cont_subreddit:
            try:
                topics_dict["title"].append(submission.title)
            except PrawcoreException as err:
                topics_dict["title"].append(err.args)
            except Exception as e:
                topics_dict["title"].append(e.__class__)
            try:
                topics_dict["score"].append(submission.score)
            except PrawcoreException as err:
                topics_dict["score"].append(err.args)
            except Exception as e:
                topics_dict["score"].append(e.__class__)
            try:
                topics_dict["id"].append(submission.id)
            except PrawcoreException as err:
                topics_dict["id"].append(err.args)
            except Exception as e:
                topics_dict["id"].append(e.__class__)
            try:
                topics_dict["url"].append(submission.url)
            except PrawcoreException as err:
                topics_dict["url"].append(err.args)
            except Exception as e:
                topics_dict["url"].append(e.__class__)
            try:
                topics_dict["comms_num"].append(submission.num_comments)
            except PrawcoreException as err:
                topics_dict["comms_num"].append(err.args)
            except Exception as e:
                topics_dict["comms_num"].append(e.__class__)
            try:
                topics_dict["created"].append(submission.created)
            except PrawcoreException as err:
                topics_dict["created"].append(err.args)
            except Exception as e:
                topics_dict["created"].append(e.__class__)
            try:
                topics_dict["body"].append(submission.selftext)
            except PrawcoreException as err:
                topics_dict["body"].append(err.args)
            except Exception as e:
                topics_dict["body"].append(e.__class__)
            try:
                topics_dict["subreddit"].append(submission.subreddit)
            except PrawcoreException as err:
                topics_dict["subreddit"].append(err.args)
            except Exception as e:
                topics_dict["subreddit"].append(e.__class__)
            try:
                topics_dict["author"].append(submission.author)
            except PrawcoreException as err:
                topics_dict["author"].append(err.args)
            except Exception as e:
                topics_dict["author"].append(e.__class__)
            try:
                topics_dict["comments"].append(submission.comments)
            except PrawcoreException as err:
                topics_dict["comments"].append(err.args)
            except Exception as e:
                topics_dict["comments"].append(e.__class__)

    topics_data = pd.DataFrame(topics_dict)
    return topics_data

def get_redditor_data(redditors):
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


    topics_dict = { "name": [],
                    "created_utc": [],
                    "has_subscribed": [],
                    "link_karma": []
                    }

    for red in redditors:
        try:
            topics_dict["name"].append(red.name)
        except PrawcoreException as err:
            topics_dict["name"].append(err.args)
        except Exception as e:
            topics_dict["name"].append(e.__class__)
        try:
            topics_dict["created_utc"].append(red.created_utc)
        except PrawcoreException as err:
             topics_dict["created_utc"].append(err.args)
        except Exception as e:
             topics_dict["created_utc"].append(e.__class__)
        try:
            topics_dict["has_subscribed"].append(red.has_subscribed)
        except PrawcoreException as err:
             topics_dict["has_subscribed"].append(err.args)
        except Exception as e:
            topics_dict["has_subscribed"].append(e.__class__)
        try:
            topics_dict["link_karma"].append(red.link_karma)
        except PrawcoreException as err:
             topics_dict["link_karma"].append(err.args)
        except Exception as e:
            topics_dict["link_karma"].append(e.__class__)

    topics_data = pd.DataFrame(topics_dict)
    return topics_data



def get_comments(reddit_object, ids):
    """
    Given an array of ids for submissions collect comments from each submission

    Returns
    -------
    None.

    """
    reddit = reddit_object

    topics_dict ={"comment_author":[], \
                  "id_from_thread":[], \
                  "comment_body":[], \
                  "comment_permalink":[],\
                  "comment_score":[]}


    for i in ids:

        submission = reddit.submission(id=i)
        submission.comments.replace_more(limit=None)

        for comment in submission.comments.list():
            try:
                topics_dict["comment_author"].append(comment.author)
            except PrawcoreException as err:
                topics_dict["comment_author"].append(err.args)
            except Exception as e:
                topics_dict["comment_author"].append(e.__class__)
            try:
                topics_dict["id_from_thread"].append(i)
            except PrawcoreException as err:
                 topics_dict["id_from_thread"].append(err.args)
            except Exception as e:
                 topics_dict["id_from_thread"].append(e.__class__)
            try:
                topics_dict["comment_body"].append(comment.body)
            except PrawcoreException as err:
                 topics_dict["comment_body"].append(err.args)
            except Exception as e:
                topics_dict["comment_body"].append(e.__class__)
            try:
                topics_dict["comment_permalink"].append(comment.permalink)
            except PrawcoreException as err:
                 topics_dict["comment_permalink"].append(err.args)
            except Exception as e:
                topics_dict["comment_permalink"].append(e.__class__)
            try:
                topics_dict["comment_score"].append(comment.score)
            except PrawcoreException as err:
                 topics_dict["comment_score"].append(err.args)
            except Exception as e:
                topics_dict["comment_score"].append(e.__class__)

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

    database = di.get_subreddit_data(reddit, subs_array, comments= comments_number, sort="new"  )

    users = di.get_redditor_data(database.author)

    final_data = pd.concat([database, users], axis=1, join="outer")

    return final_data
