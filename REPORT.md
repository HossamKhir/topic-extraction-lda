# Reporting on topic extraction with LDA

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

1. Obtaining the dataset.
2. Exploratory data analysis.
3. Feature engineering.
4. Selecting method for modelling.
5. Tuning hyper-parameters of LDA model.
6. Model training.
7. Model evaluation.
8. Assigning topics to articles.
9. Inferring topic names.

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

- using `gensim.utils.simple_preprocess` method to tokenise the article