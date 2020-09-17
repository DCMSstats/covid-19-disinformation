import pandas as pd
import disinfo as di
from disinfo import topicAnalysis
import re
import itertools

import spacy
from collections import Counter
from gensim.models.phrases import Phrases, Phraser
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from typing import List
from spacy.tokens import Doc
import re



nlp = spacy.load("en_core_web_sm")

# read in the data

submissions = pd.read_csv("../test_data/example_subs.csv")

subs = submissions

text = subs.title + subs.selftext.fillna("")

del subs 
del submissions

def tokenise2(text_list: List[str]) -> List[str]:
    """
    Remove symbols and tokenise strings

    Parameters
    ----------
    text_list: list
        a list of strings, e.g. review comments

    Returns
    -------
    tokenised_comments: a list of spacy docs
    """
    print("debug function started")
    url_regex = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
    markdown_regex = re.compile(r'\[(.+)\]\(([^ ]+?)( "(.+)")?\)')
    print("compliled regex")

    text_list = [comment.replace("’", "'") for comment in text_list]
    text_list = [comment.replace("\t", "") for comment in text_list]
    text_list = [comment.replace("\n", " ") for comment in text_list]
    text_list = [comment.replace("\n\n", " ") for comment in text_list]
    print("punct replaced")
    # handle markdown links
    text_list = [re.sub(markdown_regex, "", comment) for comment in text_list]
    print("markdown removed")
    # remove url
    text_list = [re.sub(url_regex, "", comment) for comment in text_list]
    print("url ")
    # remove multiple spaces
    text_list = [re.sub("  ", " ", comment) for comment in text_list]
    print("removd space")
    # remove amps
    #text_list = [re.sub("@", "", comment) for comment in text_list]
    print("remove amp")
    # Tokenize comments
    print("start token ")
    tokenised_comments = [nlp(comment.lower()) for comment in text_list]
    print("finish tokenn")
    return tokenised_comments



tokenise2(text)