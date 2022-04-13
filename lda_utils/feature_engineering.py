from typing import Union

from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer


def preprocess(
    document: str,
    min_len: int = 2,
    max_len: int = 15,
    stopwords: frozenset = frozenset(),
    pos: Union[str, list] = "n",
) -> str:
    """Tokenise the document, drop stopwords, then lowercase and lemmatise
    each token

    Parameters:
    -----------
    document: str
        the document to preprocess
    min_len: int
        minimum length of token, shorter tokens are discarded
    max_len: int
        maximum length of token, longer tokens are discarded
    stopwords: list, set, frozenset
        a collection of words that have little contribution to the document
        context
    pos: str, or list
        string or list of strings, which refer to a Part-of-Speech as
        described by nltk

    Returns:
    --------
    out: list
        list of tokens that has been lowercased, and lemmatised
    """
    # using gensim.utils.simple_preprocess to tokenise, lowercase a document
    pp_doc = simple_preprocess(document, min_len=min_len, max_len=max_len, deacc=True)
    # removing generic stopwords from the tokens
    doc_non_stop = [token for token in pp_doc if token not in stopwords]

    # applying text normalisation: lemmatisation
    lemmatise = WordNetLemmatizer().lemmatize
    if type(pos) == str:
        return [lemmatise(token, pos=pos) for token in doc_non_stop]
    else:
        result = doc_non_stop
        for p in pos:
            result = [lemmatise(token, pos=p) for token in result]
        return result
