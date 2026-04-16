"""Tests for the inflammation analysis script."""

from unittest.mock import patch
import numpy as np
from numpy import testing as npt

import inflammation_analysis


@patch("inflammation.compute_data.CSVDataSource.load_inflammation_data")
@patch("inflammation.views.visualize")
def test_analyse_data(mock_view, mock_load_data):
    """Test that non-full analysis visualizes each dataset separately."""

    mock_load_data.return_value = iter(
        [np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])]
    )

    inflammation_analysis.main([], full_data_analysis=False)

    assert mock_view.call_count == 2

    expected = [
        {
            "average": np.array([2.0, 3.0]),
            "max": np.array([3.0, 4.0]),
            "min": np.array([1.0, 2.0]),
        },
        {
            "average": np.array([6.0, 7.0]),
            "max": np.array([7.0, 8.0]),
            "min": np.array([5.0, 6.0]),
        },
    ]

    for call, expected_view_data in zip(mock_view.call_args_list, expected):
        assert isinstance(call.args[0], dict)
        assert set(call.args[0].keys()) == {"average", "max", "min"}
        npt.assert_array_equal(call.args[0]["average"], expected_view_data["average"])
        npt.assert_array_equal(call.args[0]["max"], expected_view_data["max"])
        npt.assert_array_equal(call.args[0]["min"], expected_view_data["min"])
