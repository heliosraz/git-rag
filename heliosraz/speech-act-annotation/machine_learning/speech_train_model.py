import numpy as np
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
import nltk
import re
import string
from sklearn.model_selection import train_test_split
from collections import defaultdict
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords

disag_df = pd.read_csv("all_speech_tags.csv", encoding="utf-8")


train_df, devtest_df, train_labels, devtest_labels = train_test_split(
    disag_df["span"], disag_df["label"], test_size=0.2, random_state=52
)
# splitting into train and dev/test

dev_df, test_df, dev_labels, test_labels = train_test_split(
    devtest_df, devtest_labels, test_size=0.5, random_state=47
)  # splitting into dev and test


def create_unigrams(df) -> defaultdict[int]:  # counting all unigrams in a dataframe
    vocabulary = defaultdict(int)
    for row in df:
        row = re.sub(r"[^\w\s]+", "", row)
        for token in row.split():
            vocabulary[token] += 1
    return vocabulary


def create_bigrams(df) -> defaultdict[int]:  # counting all bigrams in a dataframe
    vocabulary = defaultdict(int)
    for row in df:
        row = re.sub(r"[^\w\s]+", "", row)
        for token in range(len(row.split()) - 1):
            vocabulary[(row.split()[token], row.split()[token + 1])] += 1
    return vocabulary


def binary_feat_unigrams(
    df,
) -> list[defaultdict[int]]:  # checks if unigram feature is in vocab or not
    binary_features = []
    vocabulary = create_unigrams(train_df)
    for row in df:
        row_dict = defaultdict(int)
        row = re.sub(r"[^\w\s]+", "", row)
        for token in row.split():
            if token in vocabulary:
                row_dict[token] = 1
            else:
                row_dict[token] = 0
        binary_features.append(row_dict)
    return binary_features


def binary_feat_bigrams(
    df,
) -> list[defaultdict[int]]:  # checks if bigram feature is in vocab or not
    binary_features = []
    vocabulary = create_bigrams(train_df)
    for row in df:
        row_dict = defaultdict(int)
        row = re.sub(r"[^\w\s]+", "", row)
        for token in range(len(row.split()) - 1):
            if (row.split()[token], row.split()[token + 1]) in vocabulary:
                row_dict[(row.split()[token], row.split()[token + 1])] = 1
            else:
                row_dict[(row.split()[token], row.split()[token + 1])] = 0
        binary_features.append(row_dict)
    return binary_features


vectorizer1 = DictVectorizer()
config_train_1 = vectorizer1.fit_transform(binary_feat_bigrams(train_df))

clf1 = RandomForestClassifier(n_estimators=400)
clf1.fit(config_train_1, train_labels)

config_dev_1 = vectorizer1.transform(binary_feat_bigrams(dev_df))
predictions = clf1.predict(config_dev_1)

accuracy = accuracy_score(dev_labels, predictions)
report = classification_report(dev_labels, predictions)
print(accuracy)
print(report)
