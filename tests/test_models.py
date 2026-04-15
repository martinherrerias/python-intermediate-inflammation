"""Tests for statistics functions within the Model layer."""

import pytest
import numpy as np
import numpy.testing as npt

from inflammation.models import (
    load_csv,
    daily_mean,
    daily_max,
    daily_min,
    patient_normalise,
)


def test_load_csv(tmp_path):
    """Test that we can load a CSV file as a Numpy array."""

    csv_file = tmp_path / "foo.csv"
    csv_file.write_text("1,2,3\n4,5,6")
    data = load_csv(csv_file)

    npt.assert_array_equal(data, np.array([[1, 2, 3], [4, 5, 6]]))


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param([[0, 0], [0, 0], [0, 0]], [0, 0], id="all_zeros"),
        pytest.param([[1, 2], [3, 4], [5, 6]], [3, 4], id="integers"),
    ],
)
def test_daily_mean(input, expected):
    """Test that mean function works."""

    npt.assert_array_equal(daily_mean(np.array(input)), np.array(expected))


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param([[0, 0], [0, 0], [0, 0]], [0, 0], id="all_zeros"),
        pytest.param([[1, 4], [2, 3], [5, 6]], [1, 3], id="integers"),
        pytest.param([[np.nan, 4], [2, 3], [5, 6]], [np.nan, 3], id="with_nan"),
    ],
)
def test_daily_min(input, expected):
    """Test that min function works on integers."""

    npt.assert_array_equal(daily_min(np.array(input)), np.array(expected))


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param([[0, 0], [0, 0], [0, 0]], [0, 0], id="all_zeros"),
        pytest.param([[1, 4], [2, 3], [5, 6]], [5, 6], id="integers"),
        pytest.param([[np.nan, 4], [2, 3], [5, 6]], [np.nan, 6], id="with_nan"),
    ],
)
def test_daily_max(input, expected):
    """Test that min function works on integers."""

    npt.assert_array_equal(daily_max(np.array(input)), np.array(expected))


@pytest.mark.parametrize(
    "test, expected",
    [
        (
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[0.33, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]],
        )
    ],
)
def test_patient_normalise(test, expected):
    """Test normalisation works for arrays of one and positive integers.

    Test with a relative and absolute tolerance of 0.01.
    """

    result = patient_normalise(np.array(test))
    npt.assert_allclose(result, np.array(expected), rtol=1e-2, atol=1e-2)
