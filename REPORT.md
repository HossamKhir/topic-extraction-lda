# Reporting on topic extraction with LDA

- [Reporting on topic extraction with LDA](#reporting-on-topic-extraction-with-lda)
  - [Scope](#scope)
  - [Tools used](#tools-used)
  - [Pipeline](#pipeline)
    - [Obtaining the dataset](#obtaining-the-dataset)
    - [EDA](#eda)
    - [Feature Engineering](#feature-engineering)
      - [Preprocessing](#preprocessing)
    - [Method for modelling](#method-for-modelling)
    - [Tuning Hyper-Parameters of LDA](#tuning-hyper-parameters-of-lda)
      - [Tuning $k$](#tuning-k)
      - [Tuning &alpha;](#tuning-α)
    - [Model training](#model-training)
      - [Building parameters for the model](#building-parameters-for-the-model)
      - [Building the model](#building-the-model)
    - [Metrics &amp; Model evaluation](#metrics--model-evaluation)
    - [Assigning topics to articles](#assigning-topics-to-articles)
    - [Inferring topic names](#inferring-topic-names)

## Scope

Given an unlabelled dataset of articles in the medical medium, it is required to extract topics from them.

The raw data is delivered in an Excel `.xlsx` file, with a single sheet `random 5k`.

The sheet holds 3 columns:

- `ArticleID`: integer.
- `Title`: string.
- `Abstract`: string.

Reading the sheet returned $4999$ records.

---

## Tools used

To be able to work towards the scope, the following tools are used:

- Python $3.7$.
- `NumPy`.
- `Pandas` for data manipulation.
- Natural Language Tool Kit `nltk`.
- `Gensim` for topic modelling.
- `MatPlotLib` for plotting purposes.

## Pipeline

The steps taken were:

1. [Obtaining the dataset](#obtaining-the-dataset).
2. [Exploratory data analysis](#eda).
3. [Feature engineering](#feature-engineering).
4. [Selecting method for modelling](#method-for-modelling).
5. [Tuning hyper-parameters of LDA model](#tuning-hyper-parameters-of-lda).
6. [Model training](#model-training).
7. [Metrics &amp; Model evaluation](#metrics--model-evaluation).
8. [Assigning topics to articles](#assigning-topics-to-articles).
9. [Inferring topic names](#inferring-topic-names).

### Obtaining the dataset

On the local machine, the dataset was manually downloaded through the internet browser.
On Kaggle, 'twas downloaded via `wget` CLI utility.

### EDA

On loading the dataset, quick information was acquired:

- The size of the dataset was $4999$.
- The dataset had 3 columns:
  - `ArticleID`:int, which serves as UID.
  - `Title`:string, functions as a feature.
  - `Abstract`:string, functions as a feature.

Next, the string features were lowercased for ease of exploration.

The `Title` column had no issues, some titles composed of two to three words, others extended to be sentences.

The `Abstract` on the other hand had some noticeable issues.

- $5$ records contained the string `No abstract present.`
- $6$ records had the string `[Figure: see text].`, possibly a placeholder for an image tag.
- One record each containing:
  - only a `.` full-stop.
  - `N/A.`.
  - `Reply to letter`.
  - `ClinicalTrials.gov Identifier: NCT03910062.`.

### Feature Engineering

From the exploration, there seemed to be $2$ records that practically had null values (N/A &amp; simple full-stop), but the titles of these records were normal, so there was no need to drop them.
To avoid corruption or any unwanted effects, these `Abstract` fields were replaced with empty strings.

For the task, keeping the features separate is human-friendly approach,
but it doesn't bother the machine.
If any thing, makes modelling even more challenging. So both the `Title` and `Abstract` columns were combined into a single feature: `document`.
That eliminated the empty `Abstract` fields.

#### Preprocessing

on the article/record level, there was simple processing:

- using `gensim.utils.simple_preprocess` method to tokenise the article, lowercase and lemmatise each token.
- comparing the tokens against a list of stop words, to drop them.

### Method for modelling

The task were delivered with a recommendation of using `LDA` Latent Dirichlet Allocation.
After research, LDA seemed really the most fitting approach to this task.
Other candidates included `LSI` Latent Semantic Indexing and `pLSI` probabilistic LSI.

### Tuning Hyper-Parameters of LDA

When using `LDA`, the algorithm requires some hyper-parameters to be set:

- **k**: the number of topics in the corpus.
- **&alpha;**: the Dirichlet prior for document-topic distribution
- **&eta;**: also referred to as &beta; in literature, the Dirichlet prior for topic-word distribution.

Luckily, Gensim's implementation of the `LDA` model allows for setting &eta; to be learnt as if it was normal parameters.

Unfortunately, that is not always true for &alpha;.
It could be learnt in the linear implementation `LdaModel`, but cannot be learnt in the multi-core variant `LdaMulticore`,
which provides better and faster performance by exploiting multiple processors.

#### Tuning $k$

For $k$, the classical elbow method was used to determine the most likely value.
Doing so by fixing values of &alpha; and &eta; to [recommended starting values](https://stackoverflow.com/questions/39644667/rules-to-set-hyper-parameters-alpha-and-theta-in-lda-model), then fitting LDA model (refer to [Model training](#model-training)) on different values for $k$, then calculating metric score (refer to [Metrics](#metrics--model-evaluation)), then plotting the scores against $k$ to find the number of topics.

Running elbow method yielded $k=7$.

#### Tuning &alpha;

After obtaining the most likely $k$, the LDA model is fit again, but this time holding $k$ as constant, and trying different values for &alpha;,
then choosing the &alpha; that gives the highest score.
The range for &alpha; is $[0.01-1]$, as for Dirichlet distribution, &alpha; must be larger than $0$,
and stopping at $1$ as $\alpha>1$ would lead to mixed distribution, i.e. difficult to separate or assign to a certain point.

The tuned value was $\alpha=0.56$

### Model training

#### Building parameters for the model

Using Gensim model `LdaMulticore` requires parameters in certain form.

- A corpus that is in form of Bag-of-Words representation `BoW`.
- The number of topics $k$.
- A mapping of ID:word to be able to match vocabulary from the IDs in `BoW` to actual words.
- &eta; and &alpha;

So first we build the mapping using `gensim.corpora.Dictionary` object.
We make use of the dictionary's method `filter_extremes` to drop the tokens with little significance.
The insignificant token frequency was decided to be:

- Tokens occurring in less than $1\%$ of the corpus.
- Tokens occurring in more than $50\%$ of the corpus.

Then, the BoW representation is built, by making use of the dictionary method `doc2bow`.

> NOTE: this approach yields unigrams only

#### Building the model

Now the model is simply created by instantiating an instance of the `LdaMulticore` class, passing in the BoW, $k$, dictionary, &alpha;,
and possibly a `random_state` to ensure reproducible results.

### Metrics &amp; Model evaluation

Gensim provides coherence metrics, specific to the task of topic modelling.
usual metrics, like perplexity, does not always reflect the human understanding.

The metrics are provided through the class `gensim.models.CoherenceModel`,
which calculates many different coherence scores.
By default, it calculates the `C_v` score, but it is a wild score, and when initially used, gave different results with every run.
The [recommended score](https://www.baeldung.com/cs/topic-modeling-coherence-score) used was `U_mass`, which was far more persistent.

The final `U_mass` score found was $-1.4997$

### Assigning topics to articles

After fitting and evaluation an `LdaMulticore` model,
it can be easily used to return top possible topics for a given record.
Leveraging that, a data frame with index of the original dataset is returned and having features/columns of the $3$ most likely topics.

Note that, since this is in essence an unsupervised task, the topics returned are merely sorted IDs from $0,...,k-1$

### Inferring topic names

According to [Luis Serrano](https://ca.linkedin.com/in/luisgserrano) in this [video](https://www.youtube.com/watch?v=T05t-SqKArY);
labeling/naming a topic is a task that is best done by humans.

A naive approach would be to think:

    the name of the topic would be included in the vocabulary of the articles.

Working on that naive assumption:

1. The top $10$ contributing words per topic, across all topics, were collected, along with participation score for each word/topic.
1. Then examining these words, $2$ words were found to have been included in each and every topic of the $7$ topics: [*high*, *patient*]
1. Obtaining unique words/topic led to:
   1. Some topics had no unique words (remember it is subset of the top 10)
   2. Some had a single descriptive value.
   3. Others had multiple values, that are hardly informative.

The topic IDs were replaced with the most likely name of the topic.
Our topic names:

- Treatment(s).
- Cancer.
- Protein(s).

The remaining are intuitively selected based on personal reasoning:

- effect, it had a high contribution rate.
- report, as the alternative was inconclusive word `low`
- covid, had high participation, but is not unique to any topic.
- Specie, a but different word with high participation.
