from setuptools import setup, find_packages

setup(
    name="lda_utils",
    version="0.1.0",
    description="utilities used with gensim for feature engineering and topic assignments",
    author="Hossam Khair",
    author_email="hossam.khir1@outlook.com",
    packages=find_packages(["gensim", "nltk", "pandas"]),
    # TODO: complete the setup script
)
