def update_subreddit_names(reddit_object, config):
    """
    Get a list of subreddit names using a list of search terms. Append these to
    the existing list of subreddits to collect.

    Parameters
    ----------
    reddit_object : ?
    search_terms : list
    """

    project_id = config["project_id"]
    topics_list = config["topics_list"]
    table_subreddits = config["table_subreddit_list"]

    subreddits = di.get_subreddit_names(reddit_object, topics_list)

    sql = f"""
        SELECT subreddits FROM {table_subreddits}
    """
    existing_subreddits = pandas_gbq.read_gbq(query=SQL, project_id=project_id)

    subs_to_add =  subreddits[~np.isin(subreddits, existing_subreddits)]

    assert len(np.unique(subs_to_add)) == len(subs_to_add), "not all values are unique"

    subs_df =  pd.DataFrame({"subreddits": subs_to_add})
    pandas_gbq.to_gbq(subs_df, table_subreddits, project_id=project_id, if_exists="append") 


def update_submissions(reddit_object, subreddit_name)
    """
    Get a list the most recent 1000 submissions for a subreddit. Append these
    to the existing list of submissions.

    Parameters
    ----------
    reddit_object : ?
    subreddit_names : str
    """
    pass


def collect_new_comments(reddit_object, submission_id):
    """
    If new comments have been posted for a given submission, collect these.

    Parameters
    ----------
    reddit_object : ?
    subreddit_names : str
    """
    pass