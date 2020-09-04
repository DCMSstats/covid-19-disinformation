from disinfo.nlp.nlp_functions import tokenise, remove_stopwords, remove_punct

import pandas as pd
import datetime
from statistics import mean, median
from sklearn.decomposition import NMF
import pandas as pd
import numpy as np

class redditText:

    def __init__(self, df):

        self.data = df

        self.__rawTokens = tokenise(self.data.user_comment)
        self.tokens_rm_stops = remove_stopwords(self.__rawTokens)

        self.tokens = remove_punct(self.tokens_rm_stops)
        self.lemmas = [[word.lemma_ for word in comment] for comment in self.tokens]
        
    def __repr__(self):
        return(str(self.data))
