"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains
inflammation data for a single patient taken over a number of days
and each column represents a single day across all patients.
"""

from typing import TypeAlias
import numpy as np

InflammationData: TypeAlias = np.ndarray[tuple[int, int], np.dtype[np.float64]]
"""2D array of inflammation data, where rows are patients and columns are days."""

DailySummary: TypeAlias = np.ndarray[tuple[int], np.dtype[np.float64]]
"""1D array of summary statistics for each day across all patients."""


def load_csv(filename) -> InflammationData:
    """Load a Numpy array from a CSV.

    :param filename: Filename of CSV to load
    :return: 2D array of inflammation data
    """
    return np.loadtxt(fname=filename, delimiter=",")


def daily_mean(data: InflammationData) -> DailySummary:
    """Calculate the daily mean of a 2D inflammation data array."""
    return np.mean(data, axis=0)


def daily_max(data: InflammationData) -> DailySummary:
    """Calculate the daily max of a 2D inflammation data array."""
    return np.max(data, axis=0)


def daily_min(data: InflammationData) -> DailySummary:
    """Calculate the daily min of a 2D inflammation data array."""
    return np.min(data, axis=0)
