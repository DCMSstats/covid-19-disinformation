from disinfo.nlp.nlp_functions import tokenise, remove_stopwords, remove_punct

import pandas as pd
import datetime
from statistics import mean, median
from sklearn.decomposition import NMF
import pandas as pd
import numpy as np

class redditText:

    def __init__(self, df):

        columns = ["title", "selftext"]

        if not set(columns).issubset(df.columns):
            raise KeyError("Input Data does not contain the neccesary columns. Check data input and column names")

        self.data = df

        self.text = self.data.title + self.data.selftext.fillna("")

        self.__rawTokens = tokenise(self.text)
        self.__tokens_rm_stops = remove_stopwords(self.__rawTokens)

        self.tokens = remove_punct(self.__tokens_rm_stops)
        self.lemmas = [[word.lemma_ for word in comment] for comment in self.tokens]
        
    def __repr__(self):
        return(str(self.data))
