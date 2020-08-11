import os
from praw import Reddit
from praw.exceptions import MissingRequiredAttributeException

try:
    reddit = Reddit(
        client_id = os.environ.get("REDDIT_CLIENT_ID"),
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET"), 
        user_agent = os.environ.get("REDDIT_USER_AGENT")
        )
except MissingRequiredAttributeException:
    msg = (
        "REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET and REDDIT_USER_AGENT"
        "environment variables must be set to create praw.Reddit object"
    )
    raise EnvironmentError(msg)
