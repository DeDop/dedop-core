from typing import Tuple

import bokeh
import bokeh.io
import bokeh.model
import bokeh.plotting
import matplotlib.pyplot as plt
import pyproj
from bokeh.models import ColumnDataSource, Circle
from bokeh.tile_providers import STAMEN_TERRAIN
from netCDF4 import Dataset
from numpy import ndarray

from .inspect import L1bProductInspector


# (Plotting) Resources:
# * http://matplotlib.org/api/pyplot_api.html
# * http://matplotlib.org/users/image_tutorial.html
# * http://ipywidgets.readthedocs.io/en/latest/
# * http://bokeh.pydata.org/en/0.11.1/docs/user_guide/geo.html
# * http://bokeh.pydata.org/en/0.11.1/docs/user_guide/notebook.html


def compare_l1b_products(file_path_1: str, file_path_2: str, interactive=True) -> 'L1bProductInspector':
    """
    Open two L1B files for comparison.

    :param file_path_1: The file path of the first L1B product.
    :param file_path_2: The file path of the second L1B product.
    :param interactive: whether the returned comparator is supposed to run in interactive mode (i.e. IPython notebook)
    """
    return L1bProductComparator(file_path_1, file_path_2, interactive)


class L1bProductComparator:
    """
    The `L1bInspector` class provides access to L1B contents and provides a number of analysis functions.

    :param file_path_1: The file path of the first L1B product.
    :param file_path_2: The file path of the second L1B product.
    :param interactive: whether this inspector is supposed to run in interactive mode (i.e. IPython notebook)
    """

    def __init__(self, file_path_1: str, file_path_2: str, interactive):
        if not file_path_1:
            raise ValueError('file_path_1 must be given')
        if not file_path_2:
            raise ValueError('file_path_2 must be given')
        product_inspector_1 = L1bProductInspector(file_path_1, interactive)
        product_inspector_2 = L1bProductInspector(file_path_2, interactive)
        if product_inspector_1.waveform.shape != product_inspector_2.waveform.shape:
            raise ValueError('"%s" and "%s" cannot be compared as they have different waveform dimensions' % (
                file_path_1, file_path_2))

        self._product_inspector_1 = product_inspector_1
        self._product_inspector_2 = product_inspector_2
        self._plot = L1bComparisonPlotting(self, interactive)

    @property
    def p1(self) -> L1bProductInspector:
        """
        Get the first L1b file inspector.
        """
        return self._product_inspector_1

    @property
    def p2(self) -> L1bProductInspector:
        """
        Get the second L1b file inspector.
        """
        return self._product_inspector_2

    @property
    def file_path(self) -> Tuple[str, str]:
        """
        Get the L1b file path.
        """
        return self.p1.file_path, self.p2.file_path

    @property
    def dataset(self) -> Tuple[Dataset, Dataset]:
        """
        Get the underlying netCDF dataset object.
        """
        return self.p1.dataset, self.p2.dataset

    @property
    def waveform(self) -> Tuple[ndarray, ndarray]:
        """
        Get the underlying netCDF dataset object.
        """
        return self.p1.waveform, self.p2.waveform

    @property
    def plot(self) -> 'L1bComparisonPlotting':
        """
        Get the plotting context.
        """
        return self._plot

    def close(self):
        """Close the underlying dataset's file access."""
        self.p1.close()
        self.p2.close()


class L1bComparisonPlotting:
    def __init__(self, product_comparator: L1bProductComparator, interactive=True):
        self._plt = plt
        self._comparator = product_comparator
        self._interactive = interactive
        if interactive:
            bokeh.io.output_notebook(hide_banner=True)

    def locations(self):

        # Spherical Mercator
        mercator = pyproj.Proj(init='epsg:3857')
        # Equirectangular lat/lon on WGS84
        equirectangular = pyproj.Proj(init='epsg:4326')

        lon1 = self._comparator.p1.lon
        lat1 = self._comparator.p1.lat
        x1, y1 = pyproj.transform(equirectangular, mercator, lon1, lat1)

        lon2 = self._comparator.p2.lon
        lat2 = self._comparator.p2.lat
        x2, y2 = pyproj.transform(equirectangular, mercator, lon2, lat2)

        source1 = ColumnDataSource(data=dict(x=x1, y=y1))
        source2 = ColumnDataSource(data=dict(x=x2, y=y2))
        circle1 = Circle(x='x', y='y', size=6, fill_color='blue', fill_alpha=0.5, line_color=None)
        circle2 = Circle(x='x', y='y', size=6, fill_color='green', fill_alpha=0.5, line_color=None)

        # map_options = GMapOptions(lat=30.29, lng=-97.73, map_type="roadmap", zoom=11)
        # plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options)
        # plot.title.text = 'L1B Footprint'
        # plot.add_glyph(source, circle)
        # plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

        fig = bokeh.plotting.figure(x_range=(min(x1.min(), x2.min()),
                                             max(x1.max(), x2.max())),
                                    y_range=(min(y1.min(), y2.min()),
                                             max(y1.max(), y2.max())),
                                    toolbar_location='above')
        fig.axis.visible = False
        # fig.add_tile(STAMEN_TONER)
        fig.add_tile(STAMEN_TERRAIN)
        fig.title.text = "L1B Footprints"
        # fig.title = 'L1B Footprint'
        fig.add_glyph(source1, circle1)
        fig.add_glyph(source2, circle2)

        if self._interactive:
            # bokeh.io.show(plot)
            bokeh.io.show(fig)
        else:
            bokeh.io.output_file("plot_locations.html")

    def waveforms_delta_im(self, vmin=None, vmax=None):
        waveform_diff = self._comparator.p1.waveform - self._comparator.p2.waveform
        vmin = vmin if vmin else waveform_diff.min()
        vmax = vmax if vmax else waveform_diff.max()
        plt.figure(figsize=(10, 10))
        plt.imshow(waveform_diff, interpolation='nearest', aspect='auto', vmin=vmin, vmax=vmax, cmap='RdBu_r')
        plt.xlabel('Echo Sample Index')
        plt.ylabel('Time Index')
        plt.title('Waveform 1 - Waveform 2')
        plt.colorbar(orientation='vertical')
        if self._interactive:
            plt.show()
        else:
            plt.savefig("plot_waveform_diff_im.png")

    def waveforms_scatter(self):
        x = self._comparator.p1.waveform
        y = self._comparator.p2.waveform

        plt.figure(figsize=(12, 6))
        plt.scatter(x, y, alpha=0.3, edgecolors='none')
        plt.xlabel('Waveform 1')
        plt.ylabel('Waveform 2')
        plt.title('Waveforms Scatter Plot')
        plt.grid(True)
        if self._interactive:
            plt.show()
        else:
            plt.savefig("plot_waveforms_scatter.png")
