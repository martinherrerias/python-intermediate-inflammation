"""Module containing mechanism for calculating standard deviation between datasets."""

import os
from collections.abc import Iterator
import numpy as np

from inflammation import models, views
from inflammation.models import InflammationData, DailySummary

# pylint: disable=too-few-public-methods
class CSVDataSource:
    """Class to load inflammation data from a list of CSV files."""

    def __init__(self, input_files):
        """Initialise the data source with a list of input files."""

        if not isinstance(input_files, list):
            input_files = [input_files]

        for f in input_files:
            if not os.path.isfile(f):
                raise ValueError(f"Input file {f} does not exist")

        self.input_files: list[str] = input_files

    def load_inflammation_data(self) -> Iterator[InflammationData]:
        """Vectorized version of models.load_csv."""

        if len(self.input_files) == 0:
            raise ValueError("No inflammation data CSV files provided")
        yield from map(models.load_csv, self.input_files)


def compute_standard_deviation_by_day(data: Iterator[InflammationData]) -> DailySummary:
    """Calculate the standard deviation by day between datasets."""

    means_by_day = map(models.daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))
    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)
    return daily_standard_deviation


def analyse_data(data_source: CSVDataSource, visualize=True) -> None | dict:
    """Calculates the standard deviation by day between datasets.

    Gets all the inflammation data from CSV files within a directory,
    works out the mean inflammation value for each day across all datasets,
    then plots the graphs of standard deviation of these means.
    """
    data = data_source.load_inflammation_data()
    std = compute_standard_deviation_by_day(data)

    graph_data = {
        "standard deviation by day": std,
    }
    if visualize:
        views.visualize(graph_data)
        return None

    return graph_data
