"""Module containing mechanism for calculating standard deviation between datasets."""

from collections.abc import Iterator
import numpy as np

from inflammation import models, views
from inflammation.models import InflammationData


def load_inflammation_data(input_files: list) -> Iterator[InflammationData]:
    """Vectorized version of models.load_csv."""

    if len(input_files) == 0:
        raise ValueError("No inflammation data CSV files provided")
    yield from map(models.load_csv, input_files)


def analyse_data(input_files: list):
    """Calculates the standard deviation by day between datasets.

    Gets all the inflammation data from CSV files within a directory,
    works out the mean inflammation value for each day across all datasets,
    then plots the graphs of standard deviation of these means.
    """
    data = load_inflammation_data(input_files)

    means_by_day = map(models.daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))

    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)

    graph_data = {
        "standard deviation by day": daily_standard_deviation,
    }
    views.visualize(graph_data)
