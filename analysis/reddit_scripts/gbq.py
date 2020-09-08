import base64
import pandas as pd
import pandas_gbq
import praw
import numpy as np
from prawcore import PrawcoreException
import datetime


# Cloud function config
project_id =
table_sub = "
table_com =
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')
comments_number =
topics_list = []



def cache_reddit_data(event, context):
    """
    Stores reddit data
    """
    message = base64.b64decode(event['data']).decode('utf-8')
    print("DEBUG - start cache_reddit_data")

    # get the data to store

    current_data = get_reddit(topics_list, comments_number)
    current_data["created"] = current_data["created"].apply(convert_date)
    current_data["backup_date"] = datetime.date.today()
    current_data["backup_time"] = datetime.datetime.today().time()

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
    unique_data = data_to_add(newData=current_data, dataStore=df)

    # Add data to bigquery
    pandas_gbq.to_gbq(unique_data, table_sub, project_id=project_id, if_exists="append")

    # Get the comments data
    comment_data = get_comments(reddit, unique_data.id)

    # add the comment data to a seperate gbq table
    pandas_gbq.to_gbq(comment_data, table_com, project_id=project_id, if_exists="append")

    return None

# function to get data, adapted from package function
def get_reddit(topics_list, comments_number):
    print("DEBUG - get_reddit")
    subs_array = get_subreddit_names(reddit, topics_list)

    print("DEBUG- get_subreddit_data")
    database = get_subreddit_data(reddit, subs_array, comments= comments_number, sort="new"  )

    print("DEBUG- get_redditor_data")
    users = get_redditor_data(database.author)

    print("DEBUG- joining")
    final_data = pd.concat([database, users], axis=1, join="outer")

    return final_data


### ============================================================ ###
#  All functions below are taken directly from the package reddata #
### ============================================================ ###

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


def convert_date(x):
    '''
    Converts the date column from the reddit api into standard format
    '''
    return datetime.datetime.fromtimestamp(x)


def data_to_add(newData, dataStore):
    """
    Filters a pandas dataframe to only new data. Checks the newdata against the datastore
    and removes any rows which are already in the datastore returning only new data to be added to the datastore.

    Parameters
    ----------
    newData : TYPE
        DESCRIPTION.
    dataStore : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    assert 'id' in newData.columns and 'id' in dataStore.columns, 'both datasets need an id column'

    newID = newData.id.to_numpy()

    oldID = dataStore.id.to_numpy()

    id_filter = [ID in oldID for ID in newID]

    id_filter_reverse = np.invert(id_filter)

    return newData[id_filter_reverse]
