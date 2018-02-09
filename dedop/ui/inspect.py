import os.path

import bokeh
import bokeh.io
import bokeh.model
import bokeh.plotting
import bokeh.util.platform
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import pyproj
from IPython.display import display
from bokeh.models import ColumnDataSource, Circle
from bokeh.tile_providers import STAMEN_TERRAIN
from ipywidgets import interact, fixed
from matplotlib.collections import LineCollection, PolyCollection
# noinspection PyUnresolvedReferences
from mpl_toolkits.mplot3d import Axes3D
from netCDF4 import Dataset, num2date
from numpy import ndarray

from .figurewriter import FigureWriter


# (Plotting) Resources:
# * http://matplotlib.org/api/pyplot_api.html
# * http://matplotlib.org/users/image_tutorial.html
# * http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#d-plots-in-3d
# * http://ipywidgets.readthedocs.io/en/latest/
# * http://bokeh.pydata.org/en/0.11.1/docs/user_guide/geo.html
# * http://bokeh.pydata.org/en/0.11.1/docs/user_guide/notebook.html


def inspect_l1b_product(product_file_path, output_path=None, output_format=None) -> 'L1bProductInspector':
    """
    Open a L1B product for inspection.

    If *output_format* is "dir" then a new directory given by *output_path*
    will be created. Each plot figure will will be saved in a new file.

    If *output_format* is "pdf" then a new multi-page PDF document given by *output_path*
    will be created or overwritten if it exists. Each plot figure will will be saved in a new PDF page.
    Format "pdf" does not support all plot types.

    If *output_format* is not given it defaults it is derived from *output_path*.

    Note that both *output_path* and *output_format* arguments are ignored if the inspection is run in an
    Jupyter (IPython) Notebook.

    :param product_file_path: The file path of the LB product.
    :param output_path: The output path where plot figures are written to.
    :param output_format: The output format. Supported formats are "pdf" and "dir".
    """
    if output_path:
        figure_writer = FigureWriter(output_path, output_format)
    else:
        bokeh.io.output_notebook(hide_banner=True)
        figure_writer = None
    return L1bProductInspector(product_file_path, figure_writer)


class L1bProductInspector:
    """
    The `L1bInspector` class provides access to L1B contents and provides a number of analysis functions.
    """

    def __init__(self, product_file_path, figure_writer: FigureWriter):

        if not product_file_path:
            raise ValueError('product_file_path must be given')

        self._plot = L1bProductInspectorPlots(self, figure_writer)

        self._file_path = product_file_path

        dataset = Dataset(product_file_path)
        self._dataset = dataset

        self.dim_names = sorted(list(dataset.dimensions.keys()))
        self.var_names = sorted(list(dataset.variables))

        if 'time_l1bs_echo_sar_ku' in self.var_names:
            product_type = 'l1bs'
            print('WARNING: L1BS product inspection not yet fully supported.')
        elif 'time_l1b_echo_sar_ku' in self.var_names:
            product_type = 'l1b'
        else:
            raise ValueError('"%s" is neither a supported L1B nor L1BS product' % product_file_path)

        self.dim_name_to_size = {}
        for name, dim in dataset.dimensions.items():
            self.dim_name_to_size[name] = dim.size

        self.dim_names_to_var_names = {}
        for v in dataset.variables:
            dims = tuple(dataset[v].dimensions)
            if dims in self.dim_names_to_var_names:
                self.dim_names_to_var_names[dims].add(v)
            else:
                self.dim_names_to_var_names[dims] = {v}

        self.attributes = {name: dataset.getncattr(name) for name in dataset.ncattrs()}

        self.lat = dataset['lat_%s_echo_sar_ku' % product_type][:]
        self.lon = dataset['lon_%s_echo_sar_ku' % product_type][:]

        self.lat_0 = self.lat.mean()
        self.lon_0 = self.lon.mean()

        self.lat_range = self.lat.min(), self.lat.max()
        self.lon_range = self.lon.min(), self.lon.max()

        time_var = dataset['time_%s_echo_sar_ku' % product_type]
        time = time_var[:]
        self.time = num2date(time, time_var.units, calendar=time_var.calendar)
        self.time_0 = num2date(time.mean(), time_var.units, calendar=time_var.calendar)
        self.time_range = self.time.min(), self.time.max()

        waveform_counts = dataset['i2q2_meas_ku_%s_echo_sar_ku' % product_type][:]
        waveform_scaling = dataset['scale_factor_ku_%s_echo_sar_ku' % product_type][:]
        waveform_scaling = waveform_scaling.reshape(waveform_scaling.shape + (1,))

        self._waveform = waveform_scaling * waveform_counts
        self.waveform_range = self.waveform.min(), self.waveform.max()

        self.num_times = waveform_counts.shape[0]
        self.num_samples = waveform_counts.shape[1]
        self.echo_sample_ind = np.arange(0, self.num_samples)

    @property
    def file_path(self) -> str:
        """
        Get the L1b file path.
        """
        return self._file_path

    @property
    def plot(self) -> 'L1bProductInspectorPlots':
        """
        Get the plotting context.
        """
        return self._plot

    @property
    def dataset(self) -> Dataset:
        """
        Get the underlying netCDF dataset object.
        """
        return self._dataset

    @property
    def waveform(self) -> ndarray:
        """
        Get the pre-scaled waveform array.
        """
        return self._waveform

    def close(self):
        """Close the underlying dataset's file access."""
        self._dataset.close()
        self._plot.close()


class L1bProductInspectorPlots:
    def __init__(self, inspector: 'L1bProductInspector', figure_writer: FigureWriter):
        self._inspector = inspector
        self._interactive = figure_writer is None
        self._figure_writer = figure_writer

    def locations(self, color='blue'):
        """
        Plot product locations as circles onto a world map.
        """

        # Spherical Mercator
        mercator = pyproj.Proj(init='epsg:3857')
        # Equirectangular lat/lon on WGS84
        equirectangular = pyproj.Proj(init='epsg:4326')

        lon = self._inspector.lon
        lat = self._inspector.lat
        x, y = pyproj.transform(equirectangular, mercator, lon, lat)
        # print(list(zip(lon, lat)))
        # print(list(zip(x, y)))

        source = ColumnDataSource(data=dict(x=x, y=y))
        circle = Circle(x='x', y='y', size=6, fill_color=color, fill_alpha=0.5, line_color=None)

        # map_options = GMapOptions(lat=30.29, lng=-97.73, map_type="roadmap", zoom=11)
        # plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options)
        # plot.title.text = 'L1B Footprint'
        # plot.add_glyph(source, circle)
        # plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

        fig = bokeh.plotting.figure(x_range=(x.min(), x.max()), y_range=(y.min(), y.max()), toolbar_location='above')
        fig.axis.visible = False
        # fig.add_tile(STAMEN_TONER)
        fig.add_tile(STAMEN_TERRAIN)
        fig.title.text = 'L1B Locations'
        # fig.title = 'L1B Footprint'
        fig.add_glyph(source, circle)

        if self._interactive:
            bokeh.io.show(fig)
        elif self._figure_writer.output_format == "dir":
            os.makedirs(self._figure_writer.output_path, exist_ok=True)
            bokeh.io.save(fig, os.path.join(self._figure_writer.output_path, 'fig-locations.html'),
                          title='L1B Locations')
        else:
            print('warning: cannot save locations figure with output format "%s"' % self._figure_writer.output_format)

    def waveform_im(self, vmin=None, vmax=None, cmap='jet'):
        vmin = vmin if vmin else self._inspector.waveform_range[0]
        vmax = vmax if vmax else self._inspector.waveform_range[1]
        plt.figure(figsize=(10, 10))
        plt.imshow(self._inspector.waveform, interpolation='nearest', aspect='auto', vmin=vmin, vmax=vmax, cmap=cmap)
        plt.xlabel('Echo Sample Index')
        plt.ylabel('Time Index')
        plt.title('Waveform')
        plt.colorbar(orientation='vertical')
        if self._interactive:
            plt.show()
        else:
            self.savefig("fig-waveform-im.png")

    def waveform_3d_surf(self, zmin=0, zmax=None, cmap='jet'):
        self._waveform_3d(fig_type='surf', zmin=zmin, zmax=zmax, alpha=1, cmap=cmap)

    def waveform_3d_poly(self, zmin=0, zmax=None, alpha=0.5, cmap='jet'):
        self._waveform_3d(fig_type='poly', zmin=zmin, zmax=zmax, alpha=alpha, cmap=cmap)

    def waveform_3d_line(self, zmin=0, zmax=None, alpha=0.5, cmap='jet'):
        self._waveform_3d(fig_type='line', zmin=zmin, zmax=zmax, alpha=alpha, cmap=cmap)

    def _waveform_3d(self, fig_type, zmin, zmax, alpha, cmap):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.gca(projection='3d')

        num_times = self._inspector.num_times
        num_samples = self._inspector.num_samples
        if fig_type == 'surf':
            x = np.arange(0, num_samples)
            y = np.arange(0, num_times)
            x, y = np.meshgrid(x, y)
            z = self._inspector.waveform
            surf = ax.plot_surface(x, y, z, rstride=3, cstride=3, cmap=cmap, shade=True,
                                   linewidth=0, antialiased=False)
            # ax.zaxis.set_major_locator(LinearLocator(10))
            # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
            fig.colorbar(surf, shrink=0.5, aspect=5)
        else:
            waveforms = []
            for y_index in range(num_times):
                waveform = np.ndarray(shape=(num_samples, 2), dtype=np.float64)
                waveform[:, 0] = np.arange(0, num_samples)
                waveform[:, 1] = self._inspector.waveform[y_index]
                waveforms.append(waveform)
            line_widths = [0.5] * num_times
            # TODO (forman, 20160725): check why cmap is not recognized
            if fig_type == 'poly':
                edge_colors = ((0.2, 0.2, 1., 0.7),) * num_times
                face_colors = ((1., 1., 1., 0.5),) * num_times
                collection = PolyCollection(waveforms, cmap=cmap,
                                            linewidths=line_widths,
                                            edgecolors=edge_colors,
                                            facecolors=face_colors)
            else:
                colors = ((0.2, 0.2, 1., 0.7),) * num_times
                collection = LineCollection(waveforms, cmap=cmap,
                                            linewidths=line_widths, colors=colors)
            collection.set_alpha(alpha)
            ax.add_collection3d(collection, zs=np.arange(0, num_times), zdir='y')

        wf_min, wf_max = self._inspector.waveform_range
        ax.set_xlabel('Echo Sample Index')
        ax.set_xlim3d(0, num_samples - 1)
        ax.set_ylabel('Time Index')
        ax.set_ylim3d(0, num_times - 1)
        ax.set_zlabel('Waveform')
        ax.set_zlim3d(zmin if zmin is not None else wf_min, zmax if zmax is not None else wf_max)

        if self._interactive:
            plt.show()
        else:
            self.savefig("fig-waveform-3d-%s.png" % fig_type)

    def waveform_hist(self, vmin=None, vmax=None, bins=128, log=False, color='green'):
        """
        Draw waveform histogram.

        :param vmin: Minimum display value
        :param vmax: Maximum display value
        :param bins: Number of bins
        :param log: Show logarithms of bin counts
        :param color: Color of the histogram bars, e.g. 'green'
        """
        vmin = vmin if vmin else self._inspector.waveform_range[0]
        vmax = vmax if vmax else self._inspector.waveform_range[1]
        vmax = vmin + 1 if vmin == vmax else vmax

        plt.figure(figsize=(12, 6))
        plt.hist(self._inspector.waveform.flatten(),
                 range=(vmin, vmax),
                 bins=bins,
                 log=log,
                 facecolor=color,
                 alpha=1,
                 normed=True)

        plt.xlabel('Waveform')
        plt.ylabel('Counts')
        plt.title('Waveform Histogram')
        plt.grid(True)
        if self._interactive:
            plt.show()
        else:
            self.savefig("fig-waveform-hist.png")

    def waveform_line(self, ind=None, ref_ind=None):
        """
        Draw waveform 2D line plot.

        :param ind: Time index
        :param ref_ind: Reference time index
        """
        if ind is None and self._interactive:
            interact(self._plot_waveform_line, ind=(0, self._inspector.num_times - 1), ref_ind=fixed(ref_ind))
        else:
            self._plot_waveform_line(ind=ind if ind else 0, ref_ind=ref_ind)

    def _plot_waveform_line(self, ind: int, ref_ind=None):
        plt.figure(figsize=(12, 6))
        plt.plot(self._inspector.echo_sample_ind, self._inspector.waveform[ind], 'b-')
        plt.xlabel('Echo Sample Index')
        plt.ylabel('Waveform')
        plt.title('Waveform at #%s' % ind)
        plt.grid(True)

        if ref_ind is not None:
            plt.plot(self._inspector.echo_sample_ind, self._inspector.waveform[ref_ind], 'r-', label='ref')
            plt.legend(['#%s' % ind, '#%s' % ref_ind])

        if self._interactive:
            plt.show()
        else:
            self.savefig("fig-waveform-x-%d.png" % ind)

    def im(self, z=None, zmin=None, zmax=None, cmap='jet'):
        if z is None:
            if self._interactive:
                name_options = list()
                for dim_names, var_names in self._inspector.dim_names_to_var_names.items():
                    no_zero_dim = all([self._inspector.dim_name_to_size[dim] > 0 for dim in dim_names])
                    if no_zero_dim and len(dim_names) == 2:
                        name_options.extend(var_names)
                name_options = sorted(name_options)
                # TODO (forman, 20160709): add sliders for zmin, zmax
                interact(self._plot_im, z_name=name_options, zmin=fixed(zmax), zmax=fixed(zmax), cmap=fixed(cmap))
            else:
                raise ValueError('name must be given')
        else:
            self._plot_im(z_name=z, zmin=zmin, zmax=zmax, cmap=cmap)

    def _plot_im(self, z_name, zmin=None, zmax=None, cmap='jet'):
        if z_name not in self._inspector.dataset.variables:
            print('Error: "%s" is not a variable' % z_name)
            return
        var = self._inspector.dataset[z_name]
        if len(var.shape) != 2:
            print('Error: "%s" is not 2-dimensional' % z_name)
            return
        var_data = var[:]

        zmin = zmin if zmin else var_data.min()
        zmax = zmax if zmax else var_data.max()
        plt.figure(figsize=(10, 10))
        plt.imshow(self._inspector.waveform, interpolation='nearest', aspect='auto', vmin=zmin, vmax=zmax, cmap=cmap)
        # TODO (forman, 20160709): show labels in units of dimension variables
        plt.xlabel('%s (index)' % var.dimensions[1])
        plt.ylabel('%s (index)' % var.dimensions[0])
        plt.title('%s (%s)' % (z_name, var.units if hasattr(var, 'units') else '?'))
        plt.colorbar(orientation='vertical')
        if self._interactive:
            plt.show()
        else:
            self.savefig('fig-%s.png' % z_name)

    def line(self, x=None, y=None, sel_dim=False):
        """
        Plot two 1D-variables against each other.


        :param x: Name of a 1D-variable
        :param y: Name of another 1D-variable, must have the same dimension as *x*.
        :param sel_dim: Whether to display a dimension selector.
        """
        if not x or not y:
            if self._interactive:
                valid_dim_names = set()
                valid_var_names = []
                for dim_names, var_names in self._inspector.dim_names_to_var_names.items():
                    if len(dim_names) == 1 and len(var_names) > 1:
                        dim_name = dim_names[0]
                        if self._inspector.dim_name_to_size[dim_name] > 0:
                            valid_dim_names.add(dim_name)
                            valid_var_names.extend(var_names)
                valid_dim_names = sorted(valid_dim_names)
                valid_var_names = sorted(valid_var_names)
                if sel_dim:
                    widget_dim_options = valid_dim_names
                    widget_dim_value = widget_dim_options[0]

                    widget_y_options = sorted(list(self._inspector.dim_names_to_var_names[(widget_dim_value,)]))
                    widget_y_value = y if y and y in widget_y_options else widget_y_options[0]

                    widget_x_options = ['index'] + widget_y_options
                    widget_x_value = x if x and x in widget_x_options else widget_x_options[0]

                    widget_dim = widgets.Dropdown(options=widget_dim_options, value=widget_dim_value,
                                                  description='Dim:')
                    widget_x = widgets.Dropdown(options=widget_x_options, value=widget_x_value, description='X:')
                    widget_y = widgets.Dropdown(options=widget_y_options, value=widget_y_value, description='Y:')

                    display(widget_dim)

                    # noinspection PyUnusedLocal
                    def on_widget_dim_change(change):
                        nonlocal widget_x, widget_y
                        widget_y.options = sorted(list(self._inspector.dim_names_to_var_names[(widget_dim.value,)]))
                        widget_x.options = ['index'] + widget_y.options
                        widget_y.value = widget_y.options[0]
                        widget_x.value = widget_x.options[0]

                    # noinspection PyUnusedLocal
                    def on_widget_x_change(change):
                        display()

                    # noinspection PyUnusedLocal
                    def on_widget_y_change(change):
                        display()

                    widget_dim.observe(on_widget_dim_change, names='value')
                    widget_x.observe(on_widget_x_change, names='value')
                    widget_y.observe(on_widget_y_change, names='value')
                    interact(self._plot_line, x_name=widget_x, y_name=widget_y)
                else:
                    widget_x_options = ['index'] + valid_var_names
                    widget_y_options = valid_var_names
                    widget_x = widgets.Dropdown(options=widget_x_options, value=widget_x_options[0], description='X:')
                    widget_y = widgets.Dropdown(options=widget_y_options, value=widget_y_options[0], description='Y:')
                    widget_x.value = x if x and x in widget_x_options else widget_x_options[0]
                    widget_y.value = y if y and y in widget_y_options else widget_y_options[0]

                    # noinspection PyUnusedLocal
                    def on_widget_x_change(change):
                        x_name = widget_x.value
                        if x_name == 'index':
                            widget_y.options = valid_var_names
                        else:
                            widget_y.options = sorted(
                                self._inspector.dim_names_to_var_names[self._inspector.dataset[x_name].dimensions])
                        widget_y.value = widget_y.options[0]

                    widget_x.observe(on_widget_x_change, names='value')
                    interact(self._plot_line, x_name=widget_x, y_name=widget_y)

            else:
                raise ValueError('x_name and y_name must be given')
        else:
            self._plot_line(x, y)

    def _plot_line(self, x_name, y_name):
        y_var = self._inspector.dataset[y_name]
        y_units = y_var.units if hasattr(y_var, 'units') else '?'
        y_data = y_var[:]
        if x_name == 'index':
            x_units = '-'
            x_data = np.arange(0, len(y_data))
        else:
            x_var = self._inspector.dataset[x_name]
            x_units = x_var.units if hasattr(x_var, 'units') else '?'
            x_data = x_var[:]

        plt.figure(figsize=(12, 6))
        plt.plot(x_data, y_data, 'b-')
        plt.xlabel('%s (%s)' % (x_name, x_units))
        plt.ylabel('%s (%s)' % (y_name, y_units))
        # ax.set_title('%s over %s' % (x_name, y_name))
        plt.grid(True)
        if self._interactive:
            plt.show()
        else:
            self.savefig('fig-%s-over-%s.png' % (x_name, y_name))

    def im_line(self, z=None, zmin=None, zmax=None, xind=None, yind=None, cmap='jet'):
        if self._interactive:
            has_xind = xind is not None
            has_yind = yind is not None
            if not z or not has_xind or not has_yind:
                if xind is None:
                    widget_xind = widgets.IntSlider(min=0, max=10, step=1, description='X:')
                else:
                    widget_xind = fixed(xind)

                if yind is None:
                    widget_yind = widgets.IntSlider(min=0, max=10, step=1, description='Y:')
                else:
                    widget_yind = fixed(yind)

                if not z:
                    valid_var_names = list()
                    for dim_names, var_names in self._inspector.dim_names_to_var_names.items():
                        no_zero_dim = all([self._inspector.dim_name_to_size[dim] > 0 for dim in dim_names])
                        if no_zero_dim and len(dim_names) == 2:
                            valid_var_names.extend(var_names)
                    valid_var_names = sorted(valid_var_names)
                    value = z if z and z in valid_var_names else valid_var_names[0]
                    widget_var = widgets.Dropdown(options=valid_var_names, value=value, description='Var:')

                    # noinspection PyUnusedLocal
                    def on_widget_var_change(change):
                        variable = self._inspector.dataset[widget_var.value]
                        if xind is None:
                            widget_xind.max = variable.shape[1] - 1
                        if yind is None:
                            widget_yind.max = variable.shape[0] - 1

                    widget_var.observe(on_widget_var_change, names='value')
                else:
                    widget_var = fixed(z)

                # TODO (forman, 20160709): add sliders for zmin, zmax
                interact(self._plot_im_line, z_name=widget_var,
                         xind=widget_xind, yind=widget_yind,
                         zmin=fixed(zmax), zmax=fixed(zmax), cmap=fixed(cmap))
        else:
            if not z:
                raise ValueError('z_name must be given')
            self._plot_im_line(z, zmin=zmin, zmax=zmin, xind=xind, yind=yind, cmap=cmap)

    def _plot_im_line(self, z_name, zmin=None, zmax=None, xind=None, yind=None, cmap='jet'):
        assert z_name
        if z_name not in self._inspector.dataset.variables:
            print('Error: "%s" is not a variable' % z_name)
            return
        z_var = self._inspector.dataset[z_name]
        if len(z_var.shape) != 2:
            print('Error: "%s" is not 2-dimensional' % z_name)
            return

        var_data = z_var[:]

        zmin = zmin if zmin else var_data.min()
        zmax = zmax if zmax else var_data.max()

        x_title = '%s (index)' % z_var.dimensions[1]
        y_title = '%s (index)' % z_var.dimensions[0]
        z_title = '%s (%s)' % (z_name, z_var.units if hasattr(z_var, 'units') else '?')

        # TODO (forman, 20160709): show labels in units of dimension variables
        ax1, ax2, ax3, ax4 = None, None, None, None
        has_xind = xind is not None
        has_yind = yind is not None
        if has_xind and has_yind:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(12, 6))
        elif has_yind:
            fig, (ax1, ax3) = plt.subplots(2, sharex='col', figsize=(12, 6))
        elif has_xind:
            fig, (ax3, ax4) = plt.subplots(1, 2, sharey='row', figsize=(12, 6))
        else:
            fig, ax3 = plt.subplots(1, figsize=(12, 6))

        if ax1:
            z_data = z_var[yind]
            ax1.plot(np.arange(0, len(z_data)), z_data)
            ax1.grid(True)
            ax1.set_ylabel(z_title)

        if ax4:
            z_data = z_var[:, xind]
            ax4.plot(z_data, np.arange(0, len(z_data)))
            ax4.grid(True)
            ax4.set_xlabel(z_title)

        if ax2:
            # ax2.cla()
            # fig.axes.remove(ax2)
            ax2.remove()

        im = ax3.imshow(self._inspector.waveform, interpolation='nearest', aspect='auto',
                        vmin=zmin, vmax=zmax, cmap=cmap)
        if has_xind:
            ax3.axvline(x=xind)
        if has_yind:
            ax3.axhline(y=yind)
        ax3.set_xlabel(x_title)
        ax3.set_ylabel(y_title)
        if not ax1 and not ax4:
            ax3.set_title(z_title)
            fig.colorbar(im, orientation='vertical')

        if self._interactive:
            plt.show()
        elif has_xind and has_yind:
            self.savefig('fig-%s-x-%s-y-%s.png' % (z_name, xind, yind))
        elif has_xind:
            self.savefig('fig-%s-x-%s.png' % (z_name, xind))
        elif has_yind:
            self.savefig('fig-%s-y-%s.png' % (z_name, yind))
        else:
            self.savefig('fig-%s.png' % z_name)

    def savefig(self, filename):
        return self._figure_writer.savefig(filename)

    def close(self):
        if self._figure_writer:
            self._figure_writer.close()
