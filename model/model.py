import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import auc, roc_auc_score, plot_roc_curve, confusion_matrix, ConfusionMatrixDisplay, precision_recall_curve, PrecisionRecallDisplay, plot_confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

def load_pickle(file_path):
    ***REMOVED***
    Loads pickled 'combined_df' file
    ***REMOVED***

    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    return data

def establish_features_target(features, target):
    ***REMOVED***
    Returns features and target in separate 
    ***REMOVED***
    X, y = features, target

    return X, y

def main():
    # Load data
    combined_df = load_pickle('../data/combined_df.pickle')

    # Establish features/target
    X, y = establish_features_target(
        combined_df.loc[:, 'Bearish':].drop('date', axis=1),
        combined_df['5d-direction'])

    print(X.head())
    print(y.head())

if __name__ == "__main__":

    main()
