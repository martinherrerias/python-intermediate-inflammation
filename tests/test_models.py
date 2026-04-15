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


@pytest.mark.parametrize(
    "contents, expected",
    [
        pytest.param("1,2,3\n4,5,6", [[1, 2, 3], [4, 5, 6]], id="2x3 ints"),
        pytest.param("0.1,0.2,3\n4,5,6", [[0.1, 0.2, 3], [4, 5, 6]], id="2x3 float"),
        pytest.param("0,0,0", [[0, 0, 0]], id="zero row"),
        pytest.param("-1,2\n3,4", (ValueError, "negative"), id="negative"),
        pytest.param("", (ValueError, "empty"), id="empty"),
    ],
)
def test_load_csv(contents, expected, tmp_path):
    """Test that we can load a CSV file as a Numpy array."""

    csv_file = tmp_path / "foo.csv"
    csv_file.write_text(contents)

    if isinstance(expected, tuple):
        with pytest.raises(expected[0], match=expected[1]):
            data = load_csv(csv_file)
    else:
        data = load_csv(csv_file)
        npt.assert_array_equal(data, np.array(expected, ndmin=2))


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
        pytest.param([[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]], id="zeros"),
        pytest.param([[1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1]], id="ones"),
        pytest.param(
            [[1, 2, 3], [4, 5, 6]], [[0.33, 0.67, 1], [0.67, 0.83, 1]], id="ints"
        ),
    ],
)
def test_patient_normalise(test, expected):
    """Test normalisation works for arrays of one and positive integers.

    Test with a relative and absolute tolerance of 0.01.
    """

    result = patient_normalise(np.array(test))
    npt.assert_allclose(result, np.array(expected), rtol=1e-2, atol=1e-2)
