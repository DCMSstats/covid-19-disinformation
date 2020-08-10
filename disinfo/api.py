def update_subreddit_names(reddit_object, search_terms):
    """
    Get a list of subreddit names using a list of search terms. Append these to
    the existing list of subreddits to collect.

    Parameters
    ----------
    reddit_object : ?
    search_terms : list
    """
    subreddits = get_subreddit_names(reddit_object, search_terms)

    sql = f"""
        SELECT * FROM {table}
    """
    existing_subreddits = pandas_gbq.read_gbq(query=SQL, project_id=project_id)

    unique_subs = np.concatenate([subreddits, existing_subreddits[~np.isin(subreddits,existing_subreddits)]])

    return(unique_subs)

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