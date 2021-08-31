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

def encode_catgeorical_columns(X):
    ***REMOVED***
    Takes in 2 lists: a list of categorical columns and a list of numerical columns
    Outputs a concatenated dataframe with encoded categorical columns and the numerical columns
    ***REMOVED***
    categorical_columns = list(X.select_dtypes('object').columns)
    numerical_columns = list(X.select_dtypes(['int64', 'float64', 'int32', 'float32']).columns)

    ohe = OneHotEncoder(sparse=False, drop='first')
    categorical_dataframe = ohe.fit_transform(X.loc[:, categorical_columns])
    X_ohe = pd.DataFrame(
        categorical_dataframe,
        columns=ohe.get_feature_names(categorical_columns), # creates meaningful columns names
        index=X.index # Keep the same index values
    )

    # Put it all together across the columns axis
    X = pd.concat([X.loc[:, numerical_columns], X_ohe], axis=1)

    return X

def main():
    # Load data
    combined_df = load_pickle('../data/combined_df.pickle')

    # Establish features/target
    X, y = establish_features_target(
        combined_df.loc[:, 'Bearish':].drop('date', axis=1),
        combined_df['5d-direction'])

    # Encode categorical columns
    X = encode_catgeorical_columns(X)

    print(X.head())




if __name__ == "__main__":

    main()
