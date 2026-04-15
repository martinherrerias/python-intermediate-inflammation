"""Tests for compute_data."""

import pytest
import numpy as np
import numpy.testing as npt

from inflammation.compute_data import CSVDataSource


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
