# -*- coding: utf-8 -*-
"""Utils to work with datasets."""
from urllib import request
from zipfile import ZipFile

import pandas
import ucimlrepo

from common.config import Config


def get_features_and_target(id_or_url: int | tuple[str, str | list[str], str], name: str = None) -> pandas.DataFrame:
    """Get dataset by ID or URL.

    Args:
        id_or_url (int | str): Dataset ID or URL.
        name (str): Dataset name.

    Returns:
        pandas.DataFrame: Dataset with features and target.
    """
    if isinstance(id_or_url, int):
        dictdot = ucimlrepo.fetch_ucirepo(id=id_or_url)

        if name == "Auction Verification":
            dictdot.data.targets = dictdot.data.targets["verification.result"]

        if name == "Regensburg Pediatric Appendicitis":
            dictdot.data.targets = dictdot.data.targets["Diagnosis"]

        if name == "SUPPORT2":
            dictdot.data.targets = dictdot.data.targets["hospdead"]

        dataset = pandas.DataFrame(data=dictdot.data.features, columns=dictdot.data.headers)
        dataset["target"] = dictdot.data.targets
        return dataset

    url = id_or_url[0]
    datafiles = id_or_url[1] if isinstance(id_or_url[1], list) else [id_or_url[1]]
    target_name = id_or_url[2] if len(id_or_url) > 2 else None

    filepath = Config.data_dir / f"{name.lower().replace(' ',"-")}.zip"

    # Create directory if it doesn't exist
    filepath.parent.mkdir(parents=True, exist_ok=True)

    if not filepath.exists():
        request.urlretrieve(url=url, filename=filepath)

    datasets = []
    with ZipFile(filepath, "r") as zip_ref:
        for datafile in datafiles:
            datasets.append(pandas.read_csv(filepath_or_buffer=zip_ref.open(datafile)))

    datasets = datasets[0] if len(datasets) == 1 else pandas.concat(datasets)

    if target_name:
        datasets = datasets.rename(columns={target_name: "target"})

    return datasets
