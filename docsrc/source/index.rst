======================================
Welcome to pysurfline's documentation!
======================================


Get the surf forecast for any spot listed on `Surfline <https://www.surfline.com>`_.

Quickly get the forecast data as a `pandas DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ and 
plot surf forecast with `matplotlib <https://matplotlib.org/stable/>`_ to visualize the conditions of your favorite surf spot.

- **Surf** (wave min and max)
- **Wind** (speed and direction)
- **Swell** (height, period, direction)
- **Tide** (height, direction)
- **Daylight** (sunrise, sunset)

.. image:: https://github.com/giocaizzi/pysurfline/blob/gh-pages/docsrc/source/images/surfreport_readme.png
   :alt: surfreport example

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples/SpotForecast.ipynb
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
