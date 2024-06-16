# pysurfline

![SurfReport plot](https://github.com/giocaizzi/pysurfline/blob/gh-pages/docsrc/source/images/surfreport_readme.png)

**Get the surf forecast** for any spot listed on [Surfline](https://www.surfline.com/).

Quickly get the forecast data as a [pandas Dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and plot surf forecast with [matplotlib](https://matplotlib.org/stable/) to visualize the conditions of your favorite surf spot.

- **Surf** (surf min, surf max)
- **Wind** (speed, direction)
- **Swell** (height, period, direction)
- **Tide** (height, direction)
- **sunlightTimes** (sunrise, sunset)

| | |
| --- | --- |
| Distribution | ![PyPI](https://img.shields.io/pypi/v/pysurfline?color=blue) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysurfline) [![Downloads](https://static.pepy.tech/badge/pysurfline)](https://pepy.tech/project/pysurfline)|
| Builds |[![macOS](https://github.com/giocaizzi/pysurfline/actions/workflows/deployment-macos.yml/badge.svg?branch=main)](https://github.com/giocaizzi/pysurfline/actions/workflows/deployment-macos.yml)[![Ubuntu](https://github.com/giocaizzi/pysurfline/actions/workflows/deployment-ubuntu.yml/badge.svg)](https://github.com/giocaizzi/pysurfline/actions/workflows/deployment-ubuntu.yml)[![Windows](https://github.com/giocaizzi/pysurfline/actions/workflows/deployment-windows.yml/badge.svg)](https://github.com/giocaizzi/pysurfline/actions/workflows/deployment-windows.yml) |
|Tests| [![codecov](https://codecov.io/gh/giocaizzi/pysurfline/branch/main/graph/badge.svg?token=48CPYKM5BR)](https://codecov.io/gh/giocaizzi/pysurfline) |
| Documentation | [![Documentation build](https://github.com/giocaizzi/pysurfline/actions/workflows/documentation.yml/badge.svg?branch=gh-pages)](https://github.com/giocaizzi/pysurfline/actions/workflows/documentation.yml) |

## Installation

Install with `pip`

```
pip install pysurfline
```

## Example

- Get the surf forecasts for a given `SpotId` and get data as a pandas Dataframe. Control forecast timespan with `days` and `intervalHours`.

  [Go to full example.](https://giocaizzi.github.io/pysurfline/examples/SpotForecasts.html)

  ```python
  import pysurfline

  spotId = "5842041f4e65fad6a7708cfd"

  spotforecasts = pysurfline.get_spot_forecasts(
      spotId,
      days=2,
      intervalHours=3,
  )

  df = spotforecasts.get_dataframe()
  ```

- Visualize the surf report for a given `SpotId`.

  [Go to full example.](https://giocaizzi.github.io/pysurfline/examples/SurfReport.html)

  ```python
  import pysurfline

  spotId = "5842041f4e65fad6a7708cfd"

  spotforecasts = pysurfline.get_spot_forecasts(spotId)

  pysurfline.plot_surf_report(
      spotforecasts,
      barLabels=True,
  )
  ```

## Documentation

The documentation can be found [here](https://giocaizzi.github.io/pysurfline/).

## Disclaimer

This package is **not official** and **not affiliated with Surfline in any way**.

**API responses may change at any time** and the developement of this package may not be able to keep up with those changes.

If you find any issues, [please open an issue](https://github.com/giocaizzi/pysurfline/issues) or submit a [pull request](https://github.com/giocaizzi/pysurfline/pulls).
