# pysurfline

**Get the surf forecast** for any spot listed on [Surfline](https://www.surfline.com/).

Quickly get the forecast as a [pandas Dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and plot surf forecast with [matplotlib](https://matplotlib.org/stable/) to visualize the conditions of your favorite surf spot.

- **Surf** data (wave min and max)
- **Wind** data (speed and direction)
- **Swell** (height, period, direction)
- **Tide** (height, direction)
- **Daylight** (sunrise, sunset)


| | |
| --- | --- |
| Distribution | ![PyPI](https://img.shields.io/pypi/v/pysurfline?color=blue) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysurfline)
|Tests| [![Tests](https://github.com/giocaizzi/pysurfline/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/giocaizzi/pysurfline/actions/workflows/tests.yml) [![codecov](https://codecov.io/gh/giocaizzi/pysurfline/branch/main/graph/badge.svg?token=48CPYKM5BR)](https://codecov.io/gh/giocaizzi/pysurfline) |
| Code | ![black](https://img.shields.io/badge/code%20style-black-000000.svg) ![flake8](https://github.com/giocaizzi/pysurfline/actions/workflows/linting.yml/badge.svg?branch=main) |
| Documentation | [![Documentation build](https://github.com/giocaizzi/pysurfline/actions/workflows/documentation.yml/badge.svg?branch=gh-pages)](https://github.com/giocaizzi/pysurfline/actions/workflows/documentation.yml) |


# Installation

Install with `pip`
```
pip install pysurfline
```

# Example

Get the `pysurfline.SurfReport` plot for Banzai Pipeline in Oahu, Hawaii (USA).
[Go to full example.](https://giocaizzi.github.io/pysurfline/examples/surf_report.html)

![SurfReport plot](https://github.com/giocaizzi/pysurfline/blob/gh-pages/docsrc/source/images/surfreport_readme.jpeg)

# Documentation

The documentation can be found [here](https://giocaizzi.github.io/pysurfline/).
