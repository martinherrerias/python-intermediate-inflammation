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

    Values should ne non negative

    :param filename: Filename of CSV to load
    :return: 2D array of inflammation data
    """

    data = np.loadtxt(fname=filename, delimiter=",", ndmin=2)
    if np.any(data < 0):
        raise ValueError("Inflammation values should not be negative")
    if np.size(data) == 0:
        raise ValueError("Inflammation data is empty")
    return data


def daily_mean(data: InflammationData) -> DailySummary:
    """Calculate the daily mean of a 2D inflammation data array."""
    return np.mean(data, axis=0)


def daily_max(data: InflammationData) -> DailySummary:
    """Calculate the daily max of a 2D inflammation data array."""
    return np.max(data, axis=0)


def daily_min(data: InflammationData) -> DailySummary:
    """Calculate the daily min of a 2D inflammation data array."""
    return np.min(data, axis=0)


def patient_normalise(data):
    """
    Normalise patient data from a 2D inflammation data array.

    NaN values are ignored, and normalised to 0.
    """
    data_max = np.nanmax(data, axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        normalised = data / data_max[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0

    return normalised

# pylint: disable=too-few-public-methods
class Patient:
    """TODO: implement Patient model."""

    def __init__(self, args, kwargs):
        """TODO: implement Patient model."""
        raise NotImplementedError("Patient model not implemented yet")
