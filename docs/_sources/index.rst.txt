======================================
Welcome to pysurfline's documentation!
======================================


Get the surf forecasts for any spot listed on `Surfline <https://www.surfline.com>`_.

Quickly get the forecast data as a `pandas DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ and 
plot surf forecasts with `matplotlib <https://matplotlib.org/stable/>`_ to visualize the conditions of your favorite surf spot.

- **Surf** (wave min and max)
- **Wind** (speed and direction)
- **Swell** (height, period, direction)
- **Tide** (height, direction)
- **Daylight** (sunrise, sunset)

.. image:: images/surfreport_readme.png
   :alt: surfreport example

.. warning::
   This package is **not official** and **not affiliated with Surfline in any way**.

   **API responses may change at any time** and the developement of this package may not
   be able to keep up with those changes.

   If you find any issues, please open an 
   `issue <https://github.com/giocaizzi/pysurfline/issues>`_ or submit a
   `pull request <https://github.com/giocaizzi/pysurfline/pulls>`_.

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples/SpotForecasts.ipynb
   examples/SurfReport.ipynb



Code reference
==============

.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :caption: Code reference
   :recursive:

   pysurfline



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
