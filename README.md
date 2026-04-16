[![pytest](https://github.com/martinherrerias/python-intermediate-inflammation/actions/workflows/pytest.yml/badge.svg)](https://github.com/martinherrerias/python-intermediate-inflammation/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/gh/martinherrerias/python-intermediate-inflammation/branch/main/graph/badge.svg)](https://codecov.io/gh/martinherrerias/python-intermediate-inflammation)

> [!CAUTION]
> This is an example software project used in the
[Intermediate Research Software Development Skills In Python](https://github.com/carpentries-incubator/python-intermediate-development) course.

----

# Inflam
Inflam is a data management system written in Python that manages trial data used in clinical inflammation studies.

## Main features
Here are some key features of Inflam:

- Provide basic statistical analyses over clinical trial data
- Ability to work on trial data in Comma-Separated Value (CSV) format
- Generate plots of trial data
- Analytical functions and views can be easily extended based on its Model-View-Controller architecture

## Prerequisites
Inflam requires the following Python packages:

- [NumPy](https://www.numpy.org/) - makes use of NumPy's statistical functions
- [Matplotlib](https://matplotlib.org/stable/index.html) - uses Matplotlib to generate statistical plots

The following optional packages are required to run Inflam's unit tests:

- [pytest](https://docs.pytest.org/en/stable/) - Inflam's unit tests are written using pytest
- [pytest-cov](https://pypi.org/project/pytest-cov/) - Adds test coverage stats to unit testing

# Development

```sh
uv venv
source venv/bin/activate
uv sync
uv pip install -e .
inflammation --help
```
