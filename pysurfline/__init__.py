"""
python Surfline API
"""
# Version
__version__ = "0.2.1"

# Credits
__author__ = "Giorgio Caizzi"
__copyright__ = "Giorgio Caizzi, © 2022 - 2023"
__license__ = "MIT"
__maintainer__ = __author__
__email__ = "giocaizzi@gmail.com"

from pysurfline.public import get_spot_forecasts, plot_surf_report


__all__ = ["get_spot_forecasts", "plot_surf_report"]
