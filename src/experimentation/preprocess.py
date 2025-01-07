# -*- coding: utf-8 -*-
"""Preprocess data for machine learning tasks."""
import logging

import pandas
import scipy
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split


def preprocess_data(
    data: pandas.DataFrame,
    logger: logging.Logger,
) -> tuple[pandas.DataFrame, pandas.DataFrame, pandas.DataFrame, pandas.DataFrame]:
    # Lowercase column names
    data.columns = data.columns.str.lower()

    # Remove any column with only one unique value
    data = data.loc[:, data.nunique() > 1]

    # Remove any column with 100% NaN values
    data = data.loc[:, data.isnull().mean() < 1]

    # Separate features and target
    X = data.drop(columns=["target"])
    y = data["target"]

    # Identify numerical and categorical columns
    num_cols = X.select_dtypes(include=["number"]).columns.to_list()
    cat_cols = X.select_dtypes(include=["O", "object", "string"]).columns.to_list()

    logger.info(f"\t\t=> Before preprocessing:")
    logger.info(f"\t\t=> Shape X: {X.shape}, y: {y.shape}")
    logger.info(f"\t\t=> X head:\n{X.head()}")
    logger.info(f"\t\t=> y head:\n{y.head()}")
    logger.info(f"\t\t=> target proportions:\n{y.value_counts(normalize=True)}")
    logger.info(f"\t\t=> Numerical columns: {num_cols}")
    logger.info(f"\t\t=> Categorical columns: {cat_cols}")

    # Define preprocessing pipelines
    num_pipeline = Pipeline([("imputer", SimpleImputer(strategy="mean")), ("scaler", StandardScaler())])

    cat_pipeline = Pipeline(
        [("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]
    )

    preprocessor = ColumnTransformer([("num", num_pipeline, num_cols), ("cat", cat_pipeline, cat_cols)])

    # Preprocess the data
    X_preprocessed = preprocessor.fit_transform(X)

    # Drop rows with NaN values
    if scipy.sparse.issparse(X_preprocessed):
        X_preprocessed = pandas.DataFrame.sparse.from_spmatrix(X_preprocessed)

    X_preprocessed = pandas.DataFrame(X_preprocessed).dropna(axis=0, how="all")
    y = y.loc[X_preprocessed.index]

    # Drops rows with NaN values in the target
    y = pandas.DataFrame(y).dropna(axis=0, how="all")
    X_preprocessed = X_preprocessed.loc[y.index]
    y = y.values.ravel()

    logger.info(f"\t\t=> After preprocessing:")
    logger.info(f"\t\t=> Shape X: {X_preprocessed.shape}, y: {y.shape}")

    return train_test_split(X_preprocessed, y, test_size=0.4, random_state=42, stratify=y)
