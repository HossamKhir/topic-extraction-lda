import pandas as pd
from gensim.models import LdaMulticore


def get_top_n_topics(
    bow: pd.DataFrame, model: LdaMulticore, n: int = 3
) -> pd.DataFrame:
    """calculates the top `n` topics for each document in `bow` through the model

    Parameters:
    -----------
    bow: pandas.DataFrame
        the bag-of-words representation of the corpus
    model: gensim.models.ldamulticore.LdaMulticore
        the trained model to map the topics
    n: int, default = 3
        how many topics to consider to match, the default is the top three

    Returns:
    --------
    out: pandas.DataFrame
        the dataframe holding the top `n` topics, each topic_n column followed by topic_n_prop for probability
    """
    df_lda = bow.apply(
        lambda doc: sorted(model[doc], key=(lambda tup: tup[1]), reverse=True)[:n]
    )
    bow = pd.DataFrame(bow)

    for i in range(n):
        bow[f"topic_{i+1}"] = df_lda.apply(
            lambda topics: topics[i][0] if len(topics) > i else None
        )
        bow[f"topic_{i+1}_prob"] = df_lda.apply(
            lambda topics: topics[i][1] if len(topics) > i else None
        )

    # FIXME: some documents might have less than `n` possible topics
    # to avoid N/As, set them to the previous topic
    for i in range(2, n + 1):
        idx = bow[f"topic_{i}"].isna()
        cols = [f"topic_{i}", f"topic_{i}_prob"]
        cols_prev = [f"topic_{i-1}", f"topic_{i-1}_prob"]
        bow.loc[idx, cols] = bow.loc[idx, cols_prev].values

    return bow.drop(columns=["document"])
