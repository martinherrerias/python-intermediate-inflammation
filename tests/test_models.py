"""Tests for statistics functions within the Model layer."""

import pytest
import numpy as np
import numpy.testing as npt

from inflammation.models import (
    daily_mean,
    daily_max,
    daily_min,
)

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
