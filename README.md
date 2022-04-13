# Topic Extraction Using Latent Dirichlet Allocation `LDA`

Approaches to extract topics from a medical dataset using [Gensim](https://radimrehurek.com/gensim/index.html)'s [implementation](https://radimrehurek.com/gensim/models/ldamulticore.html) of Latent Dirichlet Allocation [LDA](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)

> The dataset `Pubmed5k.xlsx` was provided by [Minapharm Pharmaceuticals](http://www.minapharm.com/)

---

- [Topic Extraction Using Latent Dirichlet Allocation `LDA`](#topic-extraction-using-latent-dirichlet-allocation-lda)
  - [Setup](#setup)
  - [Usage](#usage)
  - [Directory Structure](#directory-structure)
  - [Notes](#notes)
  - [Further work](#further-work)
  - [References &amp; Resources](#references--resources)
  - [Licence](#licence)

## Setup

It is recommended to have a virtual environment set up before using this repository.

```sh

# make sure you are at the root directory of THIS repository
python3 -m venv ldaenv
source ldaenv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -e . # installs the lda_utils locally
mkdir data data/raw data/pickles

```

---

## Usage

The repository is built using [Jupyter](https://jupyter.org/) notebooks.

Simply start the Jupyter kernel, then start any notebook and run.

---

## Directory Structure

```
./
 |--data/ -> all data files (not (script or notebook))
 |  |--pickles -> all pickled files
 |  |--raw/ -> flat data files
 |--lda_utils/ -> the package directory for lda_utils module
 |--notebooks/ -> all the notebooks used in this project
 |--LICENSE -> license file
 |--README.md -> THIS file
 |--REPORT.md -> a report detailing findings
 |--requirements.txt -> required python modules by this project
 |--setup.py -> the installation script for pip to install lda_modules
```

---

## Notes

The [unigram-lda-model](./notebooks/unigram-lda-model.ipynb) notebook was run on [Kaggle](https://kaggle.com)

---

## Further work

As of date, the repository implements a unigram model, next step is to train polygram (bigram, trigram, ...) models.

---

## References &amp; Resources

The list of resources found useful for the topic of this project:

- [Text Analysis & Feature Engineering with NLP](https://towardsdatascience.com/text-analysis-feature-engineering-with-nlp-502d6ea9225d)
- [Topic Modeling and Latent Dirichlet Allocation (LDA) in Python](https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24)
- [Evaluate Topic Models: Latent Dirichlet Allocation (LDA)](https://towardsdatascience.com/evaluate-topic-model-in-python-latent-dirichlet-allocation-lda-7d57484bb5d0)
- [Topic Modeling with Latent Dirichlet Allocation](https://towardsdatascience.com/topic-modeling-with-latent-dirichlet-allocation-e7ff75290f8)
- [Understanding Topic Coherence Measures](https://towardsdatascience.com/understanding-topic-coherence-measures-4aa41339634c)
- [Latent Dirichlet Allocation(LDA): A guide to probabilistic modelling approach for topic discovery](https://towardsdatascience.com/latent-dirichlet-allocation-lda-a-guide-to-probabilistic-modeling-approach-for-topic-discovery-8cb97c08da3c)
- [Rules to set hyper-parameters alpha and theta in LDA model](https://stackoverflow.com/questions/39644667/rules-to-set-hyper-parameters-alpha-and-theta-in-lda-model)
- [What are typical values to use for alpha and beta in Latent Dirichlet Allocation?](https://stats.stackexchange.com/questions/59684/what-are-typical-values-to-use-for-alpha-and-beta-in-latent-dirichlet-allocation)
- [How does topic coherence score in LDA intuitively makes sense ?](https://stats.stackexchange.com/questions/375062/how-does-topic-coherence-score-in-lda-intuitively-makes-sense)
- [When Coherence Score is Good or Bad in Topic Modeling?](https://www.baeldung.com/cs/topic-modeling-coherence-score)
- Luis Serrano's 2 part video series on LDA: [part 1](https://www.youtube.com/watch?v=T05t-SqKArY)|[part 2](https://www.youtube.com/watch?v=BaM1uiCpj_E)
- [(Original Paper) Latent Dirichlet Allocation (algorithm)](https://www.youtube.com/watch?v=VTweNS8GiWI)

## Licence

The repository is released under GNU General Publication Licence v3.0. Please refer to [LICENSE](./LICENSE) for more information
