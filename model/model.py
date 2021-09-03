import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pickle
import warnings

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


def fxn():
    # Remove deprecation warnings
    warnings.warn("deprecated", DeprecationWarning)

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

def scale_data(X, scaler):
    ***REMOVED***
    Standardize the data for the given column
    ***REMOVED***
    scaler = scaler
    X_scaled = scaler.fit_transform(X)

    return X_scaled

def score_model(model_name, model, X, y, cv=5):
    ***REMOVED***
    Runs cross validation scores and computes the mean scores for the model performance
    ***REMOVED***
    my_model = model
    model_scores = cross_val_score(my_model, X, y, cv=cv)
    mean_model_scores = np.mean(model_scores)

    print(f"{model_name} mean score: {mean_model_scores:.4}")

    return my_model, model_scores, mean_model_scores

def find_best_model(dict_models_scores):
    ***REMOVED***
    Returns best model based on score
    ***REMOVED***
    # sort by mean scores (dict values)
    # then select the last model (highest mean scores)
    best_model = {
        k: v for k, v in sorted(
            dict_models_scores.items(), key=lambda item: item[1]
        )
    }
    best_model = list(best_model.keys())[-1]
    model_name = str(best_model)[:15]

    print(f"Best model: {model_name}")

    return best_model

def run_performance_metrics(best_model, X_scaled, X_test_scaled, y, y_test):
    ***REMOVED***
    Run a series of detailed metrics to see exactly how the model performed
    ***REMOVED***
    # Fit model
    best_model.fit(X_scaled, y)
    
    # Predictions
    preds = best_model.predict(X_test_scaled)

    # Precision
    prec_score = precision_score(y_test, preds, average='weighted')
    print(f"Precision Score: {prec_score:.4f}")

    # Recall
    rec_score = recall_score(y_test, preds, average='weighted')
    print(f"Recall Score: {rec_score:.4f}")

    # Confusion Matrix
    plot_confusion_matrix(best_model, X_test_scaled, y_test, labels=[1, 0, -1])
    plt.show();

    return prec_score, rec_score

def main():

    # Load data
    combined_df = load_pickle('../data/combined_df.pickle')

    # Establish features/target
    X, y = establish_features_target(
        combined_df.loc[:, 'Bearish':].drop('date', axis=1),
        combined_df['5d-direction'])

    # Encode categorical columns
    X = encode_catgeorical_columns(X)

    # Create holdout set (25% in this case)
    X, X_test, y, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Scale the data

    X_scaled = scale_data(X, StandardScaler())
    X_test_scaled = scale_data(X_test, StandardScaler())

    # Use cross_val_score to ross validate each model's score
    # Save the sores in a variable
    print("Calculating model scores...\n")

    knn, knn_scores, mean_knn_score = score_model('KNN',
        KNeighborsClassifier(), X_scaled, y, cv=5)

    lr, lr_scores, mean_lr_score = score_model('Logistic Regression',
        LogisticRegression(max_iter=1000), X_scaled, y, cv=5)
    
    rf, rf_scores, mean_rf_score = score_model('Random Forest',
        RandomForestClassifier(), X_scaled, y, cv=5)

    gbm, gbm_scores, mean_gbm_score = score_model('XGBoost',
        xgb.XGBClassifier(), X_scaled, y, cv=5)

    # Save above objects in a dictionary
    models_scores = {
        knn: mean_knn_score,
        lr: mean_lr_score ,
        rf: mean_rf_score,
        gbm: mean_gbm_score
    }

    # Find best model
    print("\nThe best performing model is...\n")
    best_model = find_best_model(models_scores)

    # Run Metrics
    print("\nJust running some metrics :-)")
    prec_score, rec_score = run_performance_metrics(best_model, X_scaled, X_test_scaled, y, y_test)


if __name__ == "__main__":

    main()
