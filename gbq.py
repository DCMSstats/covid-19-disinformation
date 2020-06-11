import base64
import pandas as pd
import pandas_gbq
import praw
import datetime

project_id = ""
table = ""

def cache_reddit_data(event, context):
    """
    Stores reddit data
    """
    
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    # get the data to store

    current_data = collect_reddit_data()
    
    current_data["created"] = current_data["created"].apply(convert_date)

    current_data["backup_date"] = datetime.date.today()

    current_data["backup_time"] = datetime.datetime.today().time()
    
    # find the earliest and latest date, used in the SQL query to check for duplicates
    
    earliest_date = min(current_data["created"].apply(convert_date))
    earliest_date_string =  earliest_date.strftime("%Y-%m-%d")

    latest_date = max(current_data["created"].apply(convert_date))
    latest_date_string =  latest_date.strftime("%Y-%m-%d")
    
    sql = "SELECT * FROM {0} WHERE backup_date > {1} AND backup_date < {2}"
    SQL = sql.format(table, earliest_date_string, latest_date_string) 

    # obtain data from the same period to check for duplciates

    df = pandas_gbq.read_gbq(query=SQL, project_id=project_id)
        
    # Remove duplcates
    
    unique_data = merge_data_unique(df, current_data)
    
    # Add data to bigquery
    pandas_gbq.to_gbq(unique_data, table, project_id=project_id, if_exists="append")

    return None

def collect_reddit_data():

    """
    collect reddit data and outputs a pandas dataframe
    """

    comments_number = 5
    topics_list = ["cats"]

    reddit = praw.Reddit(client_id='RNGhJE66F0dfcg',
                     client_secret='reMSAKkNv5daoHSRG3Cy15BhVw8',
                     user_agent='cdc')

    subs_array = get_subreddit_names(reddit, topics_list)

    database = get_subreddit_data(reddit, subs_array, comments= comments_number, sort="new"  )

    return(database)


# anything below is a copy and pasted function from disinfo

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



def get_subreddit_data(reddit_object, subs, comments, sort='new'):
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

        submission_dict ={'new':subreddit.new, \
                          'controversial':subreddit.controversial,\
                          'gilded':subreddit.gilded,\
                          'hot':subreddit.hot,\
                          'rising':subreddit.rising,\
                          'top':subreddit.top }


        cont_subreddit = submission_dict[sort](limit=comments)

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

def convert_date(x):
   return dt.datetime.fromtimestamp(x)

def merge_data_unique(dataset1, dataset2):
    """
    Merged two datasets returning only unique values

    Returns
    -------
    None.

    """
    
    merged = pd.merge(left=dataset1, right=dataset2, how="outer")
    
    return merged