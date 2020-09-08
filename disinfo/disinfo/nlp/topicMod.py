from disinfo.nlp.redditText import redditText
from disinfo.nlp.nlp_functions import get_phrases, calc_tfidf
from sklearn.decomposition import NMF
from statistics import median, mean
import pandas as pd
import numpy as np


class topicAnalysis(redditText):
    """
    Topic analysis class

    Produces topic analysis and outputs.

    Inherits
    --------
    redditText

    """

    def __init__(self, df):
        """
        Initialise and prepare data for analysis (ngrams and tfidf)
        """
        super().__init__(df)
        phrases = get_phrases(self.lemmas)
        self.phrases = [' '.join(i) for i in phrases]

        self.tfidf = calc_tfidf(self.phrases)

    def model_NMF(self, n_topics = 5):
        """
        Create NMF topic model

        Parameters
        ----------
        n_topics: int
            the number of topics. Defaults to 5.

        Returns
        -------
        topic_model:
            sklearn topic model (NMF)

        """

        self.n_topics = n_topics

        underlying_model = NMF(n_components = n_topics, random_state=1, alpha=.1, l1_ratio=.5,
                                      init='nndsvd')  # includes regularisation (alpha) that limits no. of topics

        self.topic_model = underlying_model.fit(self.tfidf["matrix"])

        self.review_topics = [i[1] for i in list(enumerate(self.topic_model.transform(self.tfidf["matrix"])))]

        return self.topic_model

    def get_top_words(self, n_top_words = 5):
        """
        Get the top key terms for each topic (by contribution to topic)

        Parameters
        ----------
        n_top_words: int
            the number of terms to return. Defaults to 5

        Returns
        -------
        topic_model: pd.DataFrame
            a dataframe containing the top keywords for each topic

        """

        topics = {}

        for topic_idx, topic in enumerate(self.topic_model.components_):
            topics["Topic #%d: " % topic_idx] = ([self.tfidf["features"][i] for i in topic.argsort()[:-n_top_words - 1:-1]])

        self.top_words = pd.DataFrame(topics)

        return self.top_words

    def get_dom_topics(self):
        """
        Get the dominant topic for each review and add the dominant topic and contribution to review to the data
        """

        

        dom_topic_idx = [np.where(topics == max(topics))[0] for topics in self.review_topics]
        self.data["dominant_topic"] = [row[0] if row.shape[0] == 1 else None for row in dom_topic_idx]
        self.data["p"] = [max(topics) for topics in self.review_topics]

    def get_rep_comments(self):
        """
        Get representative comments for each topic

        Returns
        -------
        examples: pd.DataFrame
            examples for each topic

        """

        if "dominant_topic" not in self.data:
            self.get_dom_topics()

        topics = {"topic": [], "example": []}

        for n in range(0, self.n_topics):
            topics["topic"].append("Topic #%d" % n)

            topic_data = self.data.loc[self.data["dominant_topic"] == n]
            topic_data.reset_index(drop=True, inplace=True)
            example = topic_data["user_comment"][topic_data["p"].argmax()]
            topics["example"].append(example)

        self.examples = pd.DataFrame(topics)

        return self.examples

    def get_topic_freqs(self):
        """
        Calculate the frequencies (counts and percentages) of each topic in the sample (as dominant topic)

        Returns
        -------
        topic_counts: pd.DataFrame
            counts and percentage frequencies for each topic
        """

        if "dominant_topic" not in self.data:
            self.get_dom_topics()

        topic_counts = self.data[["dominant_topic", "p"]].groupby("dominant_topic").count()
        self.topic_counts = topic_counts.rename(columns = {"p": "frequency"})
        self.topic_counts["percent"] = self.topic_counts["frequency"] / self.data.shape[0] * 100

        return self.topic_counts

    def output_topics(self, n_top_words = 5):
        """
        Output all examples and summary stats for each topic

        Parameters
        ----------
        n_top_words: int
            the number of top keywords to return (see get_top_words)

        Returns
        -------
        topics: pd.DataFrame
            summary statistics and examples for all topics

        """

        self.get_top_words(n_top_words)
        self.get_dom_topics()
        self.get_rep_comments()
        self.get_topic_freqs()

        topics = {
            "topic": ["Topic #%d" % i for i in list(range(0, self.n_topics))],
            "key_terms": [", ".join(data) for (name, data) in self.top_words.iteritems()],
            "example": self.examples["example"],
            "frequency": self.topic_counts["frequency"],
            "percent": self.topic_counts["percent"],
        }

        return pd.DataFrame(topics)
