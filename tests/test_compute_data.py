"""Tests for compute_data."""

import os
from glob import glob
import pytest
from unittest.mock import Mock, patch
import numpy as np
import numpy.testing as npt

from inflammation.compute_data import CSVDataSource, analyse_data


def test_csv_data_constructor(tmp_path):
    """Test CSVDataSource construction and error handling."""

    files = [tmp_path / "foo.csv", tmp_path / "bar.csv"]
    [f.touch() for f in files]

    data_source = CSVDataSource(files)
    assert data_source.input_files == files

    with pytest.raises(ValueError, match="does not exist"):
        CSVDataSource([files[0], "nonexistent.csv"])


def _random_files(tmp_path, *args):
    """Generate files with random integer tables of the given sizes."""

    files = []
    data = []
    for i, (rows, cols) in enumerate(args):
        data.append(np.random.randint(0, 10, size=(rows, cols)))
        files.append(tmp_path / f"file_{i}.csv")
        np.savetxt(files[-1], data[-1], delimiter=",")

    return files, data


@pytest.mark.parametrize(
    "file_sizes, expected_error",
    [
        pytest.param(((2, 3), (4, 5)), None, id="two ok"),
        pytest.param(((0, 0), (4, 5)), (ValueError, "empty"), id="one empty"),
        pytest.param(((2, 3),), None, id="single"),
        pytest.param((), (ValueError, "No inflammation data"), id="empty"),
    ],
)
def test_load_inflammation_data(file_sizes, expected_error, tmp_path):
    """Test that we can load a CSV file as a Numpy array."""

    csv_files, contents = _random_files(tmp_path, *file_sizes)
    data_source = CSVDataSource(csv_files)

    if expected_error is None:
        imported = data_source.load_inflammation_data()
        for data, expected in zip(imported, contents):
            npt.assert_array_equal(data, expected)
    else:
        with pytest.raises(expected_error[0], match=expected_error[1]):
            imported = list(data_source.load_inflammation_data())


@patch("inflammation.views.visualize")
def test_analyse_data(mock_view):
    """Test that we can analyse data from a CSVDataSource."""

    data_source = Mock()
    mock_data = iter([np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])])
    data_source.load_inflammation_data.return_value = mock_data

    analyse_data(data_source)

    mock_view.assert_called_once()
    graph_data = mock_view.call_args.args[0]
    npt.assert_array_equal(
        graph_data["standard deviation by day"], np.array([2.0, 2.0])
    )


def test_analyse_data_regression():
    """Test that we can analyse data from a CSVDataSource."""

    data_path = os.path.join(os.path.dirname(__file__), "../data")
    files = glob(os.path.join(data_path, "inflammation*.csv"))
    data_source = CSVDataSource(files)

    # fmt:off
    _regression_output = [
        0.,0.22510286,0.18157299,0.1264423,0.9495481,0.27118211,
        0.25104719,0.22330897,0.89680503,0.21573875,1.24235548,0.63042094,
        1.57511696,2.18850242,0.3729574,0.69395538,2.52365162,0.3179312,
        1.22850657,1.63149639,2.45861227,1.55556052,2.8214853,0.92117578,
        0.76176979,2.18346188,0.55368435,1.78441632,0.26549221,1.43938417,
        0.78959769,0.64913879,1.16078544,0.42417995,0.36019114,0.80801707,
        0.50323031,0.47574665,0.45197398,0.22070227
    ]
    # fmt:on

    result = analyse_data(data_source, visualize=False)

    npt.assert_array_almost_equal(
        result["standard deviation by day"], _regression_output
    )
