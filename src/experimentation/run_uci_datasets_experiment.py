# -*- coding: utf-8 -*-
"""Experimentation with UCI datasets."""
import json

from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

from common.config import Config
from common.log import get_logger, msg_task
from common.utils import get_features_and_target, time_it
from experimentation.evaluation import evaluate_model, append_metric
from experimentation.preprocess import preprocess_data

logger = get_logger(log_filename="uci_datasets.log")
log_error = get_logger(name="error", log_filename="error.log")


def run_experiment(
    datasets: dict[str, int | tuple[str, str | list[str]]],
    unsupervised_models: dict[str, object],
    supervised_models: dict[str, object],
) -> None:
    # Main loop to fetch datasets, preprocess, and evaluate models
    all_results = {}

    for dataset_name, id_or_url in datasets.items():

        all_results[dataset_name] = {}

        msg_task(msg=f"Dataset {dataset_name}", logger=logger)

        try:
            # Fetch dataset
            logger.info(f"\n\t=> Fetching dataset {dataset_name}")
            dataset = get_features_and_target(id_or_url=id_or_url, name=dataset_name)

            # Preprocess data
            logger.info(f"\t=> Preprocessing dataset {dataset_name}")
            X_train, X_test, y_train, y_test = preprocess_data(dataset, logger=logger)

            # Evaluate models
            logger.info(f"\n\n\t=> Training and evaluating supervised models")
            for model_name, model in supervised_models.items():
                logger.info(f"\t\t=> Training and evaluating {model_name}")
                score, total_time = time_it(
                    name=f"{dataset_name} {model_name}",
                    logger=logger,
                    funct=evaluate_model,
                    model=model,
                    supervised=True,
                    X_train=X_train,
                    X_test=X_test,
                    y_train=y_train,
                    y_test=y_test,
                )
                all_results[dataset_name][model_name] = score
                append_metric(
                    dataset=dataset_name,
                    model=model_name,
                    metric="accuracy",
                    score=score,
                    total_time=round(total_time, 4),
                )

            logger.info(f"\n\n\t=> Training and evaluating unsupervised models")
            for model_name, model in unsupervised_models.items():
                logger.info(f"\t\t=> Training and evaluating {model_name}")

                if (dataset_name == "CDC Diabetes Health Indicators" and model_name == "AgglomerativeClustering") or (
                    dataset_name == "RT-IoT2022" and model_name == "AgglomerativeClustering"
                ):
                    logger.info(f"\t\tSkipping {model_name} due to technical limitations.")
                    score = 0
                    total_time = 0.0
                else:
                    score, total_time = time_it(
                        name=f"{dataset_name} {model_name}",
                        logger=logger,
                        funct=evaluate_model,
                        model=model,
                        supervised=False,
                        X_train=X_train,
                        X_test=X_test,
                    )
                all_results[dataset_name][model_name] = score
                append_metric(
                    dataset=dataset_name,
                    model=model_name,
                    metric="silhouette",
                    score=score,
                    total_time=round(total_time, 4),
                )

            # Log results
            logger.info(f"\n\n\t=> Results for dataset {dataset_name}:\n{all_results[dataset_name]}")
        except Exception as e:
            log_error.error(f"Error with dataset {dataset_name}: {e} \n\n\n")

    # Save results to JSON
    with open(Config.project_dir / "report" / "results.json", "w") as file:
        json.dump(obj=all_results, fp=file, indent=4)


if __name__ == "__main__":
    # Datasets list:
    dataset_ids = {
        "Iris": 53,
        "Wine": 109,
        "Breast Cancer Wisconsin (Diagnostic)": 17,
        "CDC Diabetes Health Indicators": 891,
        "National Poll on Healthy Aging": 936,
        "AIDS Clinical Trials Group Study 175": 890,
        "Secondary Mushroom": 848,
        "Land Mines": 763,
        "Differentiated Thyroid Cancer Recurrence": 915,
        "Glioma Grading Clinical and Mutation Features": 759,
        "Auction Verification": 713,
        "National Health and Nutrition Health Survey 2013-2014 (NHANES) Age Prediction Subset": 887,
        "Cirrhosis Patient Survival Prediction": 878,
        "Predict Students' Dropout and Academic Success": 697,
        "RT-IoT2022": 942,
        "PhiUSIIL Phishing URL (Website)": 967,
        "Regensburg Pediatric Appendicitis": 938,
        "SUPPORT2": 880,
        "DARWIN": 732,
        "NATICUSdroid (Android Permissions)": 722,
        "Toxicity": 728,
        # To download by link: tuple(link, filename/s, target_name)
        "Period Changer": ("https://archive.ics.uci.edu/static/public/729/period+changer-2.zip", "data.csv", "Class"),
        "Sirtuin6 Small Molecules": (
            "https://archive.ics.uci.edu/static/public/748/sirtuin6+small+molecules-1.zip",
            "SIRTUIN6.csv",
            "Class",
        ),
    }

    # Define models
    unsupervised_catalog = {
        "KMeans": KMeans(n_clusters=3, max_iter=100),
        "DBSCAN": DBSCAN(n_jobs=-1),
        "MiniBatchKMeans": MiniBatchKMeans(n_clusters=3),
    }

    supervised_catalog = {
        "RandomForest": RandomForestClassifier(max_depth=15, n_jobs=-1),
        "KNeighbors": KNeighborsClassifier(n_jobs=-1),
        "LogisticRegression": LogisticRegression(n_jobs=-1, max_iter=100),
    }

    run_experiment(datasets=dataset_ids, unsupervised_models=unsupervised_catalog, supervised_models=supervised_catalog)
