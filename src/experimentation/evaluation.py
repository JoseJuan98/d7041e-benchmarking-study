# -*- coding: utf-8 -*-
"""Evaluation of models."""
from typing import Type

import numpy
import pandas
import sklearn
from common.config import Config
from sklearn.metrics import accuracy_score, silhouette_score


def evaluate_model(
    model: Type[sklearn.base],
    supervised: bool,
    X_train: numpy.ndarray | pandas.DataFrame,
    X_test: numpy.ndarray | pandas.DataFrame,
    y_train: numpy.ndarray | pandas.DataFrame = None,
    y_test: numpy.ndarray | pandas.DataFrame = None,
) -> float:
    # Evaluate supervised models
    if supervised:
        model.fit(X_train, y_train)
        test_score = accuracy_score(y_true=y_test, y_pred=model.predict(X_test))

    # Evaluate unsupervised models
    else:
        model.fit(X_train)

        # To avoid: ValueError: Number of labels is 1. Valid values are 2 to n_samples - 1 (inclusive)
        if len(set(model.labels_)) == 1:
            test_score = 0.0
        else:
            test_score = silhouette_score(X_test, model.fit_predict(X_test)).item()

        # if isinstance(test_score, numpy.ndarray):
        #     test_score = test_score.item()

    return round(test_score, 4)


def append_metric(metric: str, dataset: str, model: str, total_time: float, score: float) -> None:
    """Append the metric to the metrics file.

    Args:
        dataset (str): The dataset used.
        metric (str): The metric to append.
        model (str): The model used.
        total_time (float): The total time taken to evaluate the model.
        score (float): The score of the model.
    """
    metrics_path = Config.project_dir / "report" / "metrics.txt"

    # Create directory if it doesn't exist
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    with open(metrics_path, "a") as file:
        file.write(f"{dataset},{model},{metric},{score},{total_time}\n")
