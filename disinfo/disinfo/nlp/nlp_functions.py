import spacy
from collections import Counter
from gensim.models.phrases import Phrases, Phraser
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer

nlp = spacy.load("en_core_web_sm")

def tokenise(text_list):
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
    # Remove symbols
    text_list = [comment.replace("’", "'") for comment in text_list]
    text_list = [comment.replace("\t", "") for comment in text_list]
    text_list = [comment.replace("\n", " ") for comment in text_list]
    text_list = [comment.replace("\n\n", " ") for comment in text_list]

    # Tokenize comments
    tokenised_comments = [nlp(comment) for comment in text_list]

    return tokenised_comments


def remove_stopwords(tokens):
    """
    Remove stopwords from lists of tokens

    Parameters
    ----------
    tokens: list
        a nested list containing lists of tokens or a list of spacy docs

    Returns
    -------
    filtered_comments: list
        nested lists of tokens

    """

    from spacy.lang.en.stop_words import STOP_WORDS
    custom_stops = [" ", "app"] # Move custom stops to config file later

    filtered_comments = [[token for token in comment if nlp.vocab[token.text].is_stop == False and token.text not in custom_stops] for comment in tokens]

    return filtered_comments


def remove_punct(tokens):
    """
    Remove punctuation marks from lists of tokens

    Parameters
    ----------
    tokens: list
        a nested list containing lists of tokens or a list of spacy docs

    Returns
    -------
    filtered_comments: list
        nested lists of tokens

    """

    filtered_comments = [[token for token in comment if nlp.vocab[token.text].is_punct == False] for comment in tokens]

    return filtered_comments


def lemmatise(tokens):
    """
    Lemmatise nested list of tokens

    Parameters
    ----------
    tokens: list
        a nested list containing lists of tokens or a list of spacy dcs

    Returns
    -------
    lemmas: list
        a nested list of lemmas

    """

    lemmas = [[word.lemma_ for word in comment] for comment in tokens]

    return lemmas


def count_words(tokens, n_words = 20):
    """
    Count the number of comments containing each entry

    Parameters
    ----------
    tokens: list
        a nested list containing lists of tokens or a list of spacy docs
    n: int
        The number of words to return. Defaults to 20, i.e. the top 20 words

    Returns
    -------
    word_freq(most_common(n)): a list of tuples
        a list of tuples containing words and frequencies

    """

    # Flatten list and set to lower case
    bag_of_words = [word.lower() for comment in tokens for word in comment]
    unique_words = set(bag_of_words)

    word_counts = []

    for word in unique_words:
        n = 0
        for doc in tokens:
            if word in doc:
                n += 1
        word_counts.append((word, n))

    word_counts.sort(key = lambda x: x[1], reverse = True)

    return word_counts[0:n_words]


def keyword_filter(df, keywords, column = "user_comment", mode = "include"):
    """
    Produce mask to filter dataframe by keywords

    Parameters
    ----------
    df: pandas.DataFrame
        a dataframe to be filtered
    keywords: list of strings
        a list of keywords to filter by (lemmas, lower case)
    column: string
        the name of the column containing the filter text. Defaults to "user_comments"
    mode: string
        the filter mode. "include" to include only matching cases, "exclude" to remove all matching cases. Defaults to "include"

    Returns
    -------
    filter: list of bools
        a mask that can be used to filter pandas.DataFrame rows

    """

    filter_word_list = tokenise(df[column])
    filter_word_list = remove_stopwords(filter_word_list)
    filter_word_list = lemmatise(filter_word_list)

    filter = [bool(set(comment).intersection(set(keywords))) for comment in filter_word_list]

    if mode == "exclude":
        filter = [not i for i in filter]

    return(filter)


def chunk_it(token_list):
    """
    Compute noun chunks from Spacy docs

    Parameters
    ----------
    token_list: list of spacy docs

    Returns
    -------
    chunks: list of lists
        a list containing lists of noun chunks
    """

    chunks = [comment.noun_chunks for comment in token_list]

    return chunks


def get_phrases(texts) -> list:
    try:
        texts = [[word.lower() for word in comment] for comment in texts]
    except: # If items are Spacy tokens not strings
        texts = [[word.text.lower() for word in comment] for comment in texts]

    phrases = Phrases(texts, min_count=1, threshold=2)
    bigram = Phraser(phrases)  # do learning

    tg_phrases = Phrases(bigram[texts], threshold=2)
    trigram = Phraser(tg_phrases)

    texts = trigram[texts]

    return texts

def calc_tfidf(texts: list, char_ngrams=False, stop_words=None, max_features=20000) -> object:

    token_pattern_2_char = r"(?u)\b\w\w+\b"  # original

    if char_ngrams:
        analyzer, ngrams = 'char', (1, 4)
    else:
        analyzer, ngrams = 'word', (1, 3)

    output = {}

    # count vectorize tokens
    count_vectorizer = CountVectorizer(tokenizer=None, max_df = .5, min_df = 2,
                                       ngram_range=ngrams, max_features=max_features,
                                       binary=False, analyzer=analyzer, token_pattern=token_pattern_2_char)
    count_matrix = count_vectorizer.fit_transform(texts)

    output["features"] = count_vectorizer.get_feature_names()

    tfidf_transformer = TfidfTransformer(use_idf = True)
    output["matrix"] = tfidf_transformer.fit_transform(count_matrix)

    return output
