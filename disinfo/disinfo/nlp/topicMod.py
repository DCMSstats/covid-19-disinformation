from disinfo.nlp.redditText import redditText
from disinfo.nlp.nlp_functions import get_phrases, calc_tfidf
from sklearn.decomposition import NMF, LatentDirichletAllocation
from statistics import median, mean
import pandas as pd
import numpy as np
import gensim.corpora as corpora
from gensim.models import CoherenceModel
import gensim
from tqdm import tqdm


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
  
        self.__joined = [' '.join(i) for i in self.lemmas]

        self.tfidf = calc_tfidf(self.__joined)

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

    def model_LDA(self, n_topics = 5):
        """

        """

        self.n_topics = n_topics

        underlying_model = LatentDirichletAllocation(n_components = n_topics, max_iter = 10, learning_method = 'online', verbose = True)

        self.topic_model = underlying_model.fit(self.tfidf["count matrix"])

        self.review_topics = [i[1] for i in list(enumerate(self.topic_model.transform(self.tfidf["count matrix"])))]

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

        if not hasattr(self, 'topic_model'):
            raise AttributeError("topic model attribute does not exist. You need to run one of the available topic models first, e.g model_lda or model_NMF")

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

    def model_evaluation(self, corpus, id2word, topic_number = 5, alpha = 'symmetric', beta= 'symmetric'):
        """
        Calculates the topic coherence score for an LDA model.

        Parameters
        ----------
        corpus: iterable of list of (int, float)
            Stream of document vectors or sparse matrix of shape
        id2word: dict of (int, str)
            Mapping from word IDs to words.
        topic_number: List of Int e.g [5], [3,4,7,8], range(5,10)
            The number of requested latent topics to be extracted from the training corpus.
        alpha: np.ndarray, str
            Dirichlet hyperparameter alpha: Document-Topic Density - Can be set to an 1D array of length equal to the number of expected topics that expresses our a-priori belief for the each topics’ probability
        beta: float, np.array, str
            Dirichlet hyperparameter beta: Word-Topic Density - A-priori belief on word probability.

        Returns
        ----------
        coherence_lda: Float
            A single value which expresses the topic coherence for the given model

        """

        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=topic_number,
                                            random_state=100,
                                            chunksize=100,
                                            passes=10,
                                            alpha = alpha,
                                            eta= beta,
                                            per_word_topics=True)

        coherence_model_lda = CoherenceModel(model=lda_model, texts=self.lemmas, dictionary=id2word, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        #print(f"Coherence Score: {coherence_lda} for number of topic = {topic_number}, alpha = {alpha} and beta = {beta} ")

        return coherence_lda

    def calculate_model_score(self, topic_num = None, alpha = None, beta= None):
        """
        Calculates the topic coherence scores for a range of LDA models

        Parameters:
        ---------------
        topic_number: List of Int, optional. e.g [5], [3,4,7,8], range(5,10)
            The number of requested latent topics to be extracted from the training corpus. Defaults to a range(4,8)
        alpha: {np.ndarray, str} optinal
            Dirichlet hyperparameter alpha: Document-Topic Density - Can be set to an 1D array of length equal to the number of expected topics that expresses our a-priori belief for the each topics’ probability.
            Defaults - [0.01, 0.31, 0.61, 0.9099999999999999, 'symmetric', 'asymmetric']
        beta: {float, np.array, str}, optional
            Dirichlet hyperparameter beta: Word-Topic Density - A-priori belief on word probability.
            Defaults - [0.01, 0.31, 0.61, 0.9099999999999999, 'symmetric']

        Returns
        -------
        model_score: pd.DataFrame
            A dataframe containg the coherence score for wach model permuation
        """

        # Process lemmas for gensim LDA model
        id2word = corpora.Dictionary(self.lemmas)

        # Term Document Frequency
        corpus = [id2word.doc2bow(text) for text in self.lemmas]


        # Default Arguments
        if topic_num is None:
            topic_num =  range(4,8)

        if alpha is None:
            alpha = list(np.arange(0.01, 1, 0.3))
            alpha.append('symmetric')
            alpha.append('asymmetric')

        if beta is None:
            beta = list(np.arange(0.01, 1, 0.3))
            beta.append('symmetric')

        total_models_to_run = len(topic_num) * len(alpha) * len(beta)

        print(f"You have selected {total_models_to_run} models to run. This make take some time...")

        model_score = {
                "coherence_score": [],
                "topic_num": [],
                "alpha": [],
                "beta": []
            }

        with tqdm(total = total_models_to_run) as pbar:
            for i in topic_num:
                for al in alpha:
                    for be in beta:
                        model = self.model_evaluation(corpus, id2word, topic_number=i, alpha=al, beta=be)
                        model_score["coherence_score"].append(model)
                        model_score["topic_num"].append(i)
                        model_score["alpha"].append(al)
                        model_score["beta"].append(be)
                        pbar.update(1)

        return pd.DataFrame(model_score)