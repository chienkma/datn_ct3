from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from time import time
from sklearn.metrics import f1_score
from os import path, makedirs
from joblib import dump, load
import json

# Utility Functions


def train_classifier(clf, X_train, y_train):
    start = time()
    clf.fit(X_train, y_train)
    end = time()
    print("Model trained in {:2f} seconds".format(end - start))


def predict_labels(clf, features, target):
    start = time()
    y_pred = clf.predict(features)
    end = time()
    print("Made Predictions in {:2f} seconds".format(end - start))

    acc = sum(target == y_pred) / float(len(y_pred))

    return f1_score(target, y_pred, average="micro"), acc


def model(clf, X_train, y_train, X_test, y_test):
    train_classifier(clf, X_train, y_train)

    f1, acc = predict_labels(clf, X_train, y_train)
    print("Training Info:")
    print("-" * 20)
    print("F1 Score:{}".format(f1))
    print("Accuracy:{}".format(acc))

    f1, acc = predict_labels(clf, X_test, y_test)
    print("Test Metrics:")
    print("-" * 20)
    print("F1 Score:{}".format(f1))
    print("Accuracy:{}".format(acc))


# Data gathering

en_data_folder = "english-premier-league"
es_data_folder = "spanish-la-liga"
fr_data_folder = "french-ligue-1"
ge_data_folder = "german-bundesliga"
it_data_folder = "italian-serie-a"

# data_folders = [es_data_folder]
data_folders = [
    en_data_folder,
    es_data_folder,
    fr_data_folder,
    ge_data_folder,
    it_data_folder,
]

season_range = (13, 22)

data_files = []
for data_folder in data_folders:
    for season in range(season_range[0], season_range[1] + 1):
        data_files.append(
            "data/{}/data/season-{:02d}.csv".format(data_folder, season, season + 1)
        )

data_frames = []

for data_file in data_files:
    if path.exists(data_file):
        data_frames.append(pd.read_csv(data_file))

data = pd.concat(data_frames).reset_index()
print(data)

# Pre processing

input_filter = [
    "home_encoded",
    "away_encoded",
    "HTHG",
    "HTAG",
    "HS",
    "AS",
    "HST",
    "AST",
    "HR",
    "AR",
]
output_filter = ["FTR"]

cols_to_consider = input_filter + output_filter

encoder = LabelEncoder()
home_encoded = encoder.fit_transform(data["HomeTeam"])
home_encoded_mapping = dict(
    zip(encoder.classes_, encoder.transform(encoder.classes_).tolist())
)
data["home_encoded"] = home_encoded

encoder = LabelEncoder()
away_encoded = encoder.fit_transform(data["AwayTeam"])
away_encoded_mapping = dict(
    zip(encoder.classes_, encoder.transform(encoder.classes_).tolist())
)
data["away_encoded"] = away_encoded

data = data[cols_to_consider]

print(data[data.isna().any(axis=1)])
data = data.dropna(axis=0)

# Training & Testing

X = data[input_filter]
Y = data["FTR"]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

lr_classifier = LogisticRegression(multi_class="ovr", max_iter=500)
nbClassifier = GaussianNB()
rfClassifier = RandomForestClassifier()


print()
print("Logistic Regression one vs All Classifier")
print("-" * 20)
model(lr_classifier, X_train, Y_train, X_test, Y_test)

print()
print("Gaussain Naive Bayes Classifier")
print("-" * 20)
model(nbClassifier, X_train, Y_train, X_test, Y_test)


print()
print("Random Forest Classifier")
print("-" * 20)
model(rfClassifier, X_train, Y_train, X_test, Y_test)

# Exporting the Model
print()
print()
shouldExport = input("Do you want to export the model(s) (y / n) ? ")
if shouldExport.strip().lower() == "y":
    exportedModelsPath = "exportedModels"

    makedirs(exportedModelsPath, exist_ok=True)

    dump(lr_classifier, f"{exportedModelsPath}/lr_classifier.model")
    dump(nbClassifier, f"{exportedModelsPath}/nb_classifier.model")
    dump(rfClassifier, f"{exportedModelsPath}/rf_classifier.model")

    exportMetaData = dict()
    exportMetaData["home_teams"] = home_encoded_mapping
    exportMetaData["away_teams"] = away_encoded_mapping

    exportMetaDataFile = open(f"{exportedModelsPath}/metaData.json", "w")
    json.dump(exportMetaData, exportMetaDataFile)

    print(f"Model(s) exported successfully to {exportedModelsPath}/")

    lr_model = load("exportedModels/lr_classifier.model")
    print(lr_model)
    rf_model = load("exportedModels/rf_classifier.model")
    print(rf_model)
    nb_model = load("exportedModels/nb_classifier.model")
    print(nb_model)
