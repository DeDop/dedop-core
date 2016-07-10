import sys

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display
from ipywidgets import interact, fixed
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset, num2date


# Resources:
# * http://matplotlib.org/api/pyplot_api.html
# * http://matplotlib.org/users/image_tutorial.html
# * http://matplotlib.org/basemap/users/examples.html
# * http://ipywidgets.readthedocs.io/en/latest/



class L1bAnalysis:
    def __init__(self, file, interactive=True):
        self.plt = plt

        self.file = file
        self.interactive = interactive

        ds = Dataset(file)
        self.ds = ds

        self.dim_name_to_size = {}
        for name, dim in ds.dimensions.items():
            self.dim_name_to_size[name] = dim.size

        self.dim_names_to_var_names = {}
        for v in ds.variables:
            dims = tuple(ds[v].dimensions)
            if dims in self.dim_names_to_var_names:
                self.dim_names_to_var_names[dims].add(v)
            else:
                self.dim_names_to_var_names[dims] = {v}

        self.attributes = {name: self.ds.getncattr(name) for name in self.ds.ncattrs()}

        self.lat = ds['lat_l1b_echo_sar_ku'][:]
        self.lon = ds['lon_l1b_echo_sar_ku'][:] - 180.0

        self.lat_0 = self.lat.mean()
        self.lon_0 = self.lon.mean()

        self.lat_range = self.lat.min(), self.lat.max()
        self.lon_range = self.lon.min(), self.lon.max()

        time_var = ds['time_l1b_echo_sar_ku']
        time = time_var[:]
        self.time = num2date(time, time_var.units, calendar=time_var.calendar)
        self.time_0 = num2date(time.mean(), time_var.units, calendar=time_var.calendar)
        self.time_range = self.time.min(), self.time.max()

        meas = ds['i2q2_meas_ku_l1b_echo_sar_ku'][:]
        scale_factor = ds['scale_factor_ku_l1b_echo_sar_ku'][:]
        scale_factor = scale_factor.reshape(scale_factor.shape + (1,))

        self.meas = scale_factor * meas
        self.meas_range = self.meas.min(), self.meas.max()

        self.num_times = meas.shape[0]
        self.num_samples = meas.shape[1]
        self.echo_sample_ind = np.arange(0, self.num_samples)

    def close(self):
        self.ds.close()

    def plot_locs(self, scales=None):
        lat_0 = self.lat.mean()
        lon_0 = self.lon.mean()

        if not scales:
            scales = [20, 10, 5, 1.2]

        m = Basemap(projection='tmerc', lat_0=lat_0, lon_0=lon_0, width=10000, height=10000)
        x, y = m(self.lon, self.lat)
        size = max(x.max() - x.min(), y.max() - y.min())
        fig, axes = plt.subplots(nrows=1, ncols=len(scales), figsize=(20, 20))
        for axis, scale in zip(axes, scales):
            width = scale * size
            height = scale * size
            m = Basemap(ax=axis, projection='tmerc', lat_0=lat_0, lon_0=lon_0, width=width, height=height)
            x, y = m(self.lon, self.lat)
            m.drawmapboundary(fill_color='#99FFFF')
            m.fillcontinents(color='#CC9966', lake_color='#99FFFF')
            m.scatter(x, y, s=10, marker='o', color='blue')
            axis.set_title('%s x' % scale, fontsize=12)
        if self.interactive:
            plt.show()
        else:
            plt.savefig("plot_locs.png")

    def plot_meas_im(self, vmin=None, vmax=None):
        vmin = vmin if vmin else self.meas_range[0]
        vmax = vmax if vmax else self.meas_range[1]
        plt.figure(figsize=(10, 10))
        plt.imshow(self.meas, interpolation='nearest', aspect='auto', vmin=vmin, vmax=vmax)
        plt.xlabel('echo_sample_ind')
        plt.ylabel('time_ind')
        plt.title('i2q2_meas_ku')
        plt.colorbar(orientation='vertical')
        if self.interactive:
            plt.show()
        else:
            plt.savefig("plot_meas_im.png")

    def plot_meas_hist(self, vmin=None, vmax=None, bins=128, log=False):
        vmin = vmin if vmin else self.meas_range[0]
        vmax = vmax if vmax else self.meas_range[1]

        # mu, sigma = 100, 15
        # x = mu + sigma * np.random.randn(10000)

        # the histogram of the data
        plt.figure(figsize=(12, 6))
        n, bins, patches = plt.hist(self.meas.flatten(),
                                    range=(vmin, vmax),
                                    bins=bins,
                                    log=log,
                                    facecolor='green',
                                    alpha=1,
                                    normed=True)

        # add a 'best fit' line
        # y = mlab.normpdf(bins, mu, sigma)
        # l = plt.plot(bins, y, 'r--', linewidth=1)

        plt.xlabel('i2q2_meas_ku')
        plt.ylabel('probability')
        # plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
        plt.title('Histogram of i2q2_meas_ku')
        # plt.axis([40, 160, 0, 0.03])
        plt.grid(True)
        if self.interactive:
            plt.show()
        else:
            plt.savefig("plot_meas_hist.png")

    def plot_meas(self, ind=None, ref_ind=None):
        if ind is None and self.interactive:
            interact(self._plot_meas, ind=(0, self.num_times - 1), ref_ind=fixed(ref_ind))
        else:
            self._plot_meas(ind=ind if ind else 0, ref_ind=ref_ind)

    def _plot_meas(self, ind: int, ref_ind=None):
        plt.figure(figsize=(12, 6))
        plt.plot(self.echo_sample_ind, self.meas[ind], 'b-')
        plt.xlabel('echo_sample_ind')
        plt.ylabel('i2q2_meas_ku')
        plt.title('i2q2_meas_ku #%s' % ind)
        plt.grid(True)

        if ref_ind is not None:
            plt.plot(self.echo_sample_ind, self.meas[ref_ind], 'r-', label='ref')
            plt.legend(['#%s' % ind, '#%s' % ref_ind])

        if self.interactive:
            plt.show()
        else:
            plt.savefig("plot_meas_t%06d.png" % ind)

    # TODO - remove
    def plot_1d_vars(self, x_name=None, y_name=None, sel_dim=False):
        if not x_name or not y_name:
            if self.interactive:
                valid_dim_names = set()
                valid_var_names = []
                for dim_names, var_names in self.dim_names_to_var_names.items():
                    if len(dim_names) == 1 and len(var_names) > 1:
                        dim_name = dim_names[0]
                        if self.dim_name_to_size[dim_name] > 0:
                            valid_dim_names.add(dim_name)
                            valid_var_names.extend(var_names)
                valid_dim_names = sorted(valid_dim_names)
                valid_var_names = sorted(valid_var_names)
                if sel_dim:
                    widget_dim_options = valid_dim_names
                    widget_dim_value = widget_dim_options[0]

                    widget_y_options = sorted(list(self.dim_names_to_var_names[(widget_dim_value,)]))
                    widget_y_value = widget_y_options[0]

                    widget_x_options = ['index'] + widget_y_options
                    widget_x_value = widget_x_options[0]

                    widget_dim = widgets.Dropdown(options=widget_dim_options, value=widget_dim_value,
                                                  description='Dim:')
                    widget_x = widgets.Dropdown(options=widget_x_options, value=widget_x_value, description='X:')
                    widget_y = widgets.Dropdown(options=widget_y_options, value=widget_y_value, description='Y:')

                    display(widget_dim)

                    def on_widget_dim_change(change):
                        nonlocal widget_x, widget_y
                        widget_y.options = sorted(list(self.dim_names_to_var_names[(widget_dim.value,)]))
                        widget_x.options = ['index'] + widget_y.options
                        widget_y.value = widget_y.options[0]
                        widget_x.value = widget_x.options[0]

                    def on_widget_x_change(change):
                        display()

                    def on_widget_y_change(change):
                        display()

                    widget_dim.observe(on_widget_dim_change, names='value')
                    widget_x.observe(on_widget_x_change, names='value')
                    widget_y.observe(on_widget_y_change, names='value')
                    interact(self._plot_1d_vars, x_name=widget_x, y_name=widget_y)
                else:
                    widget_x_options = ['index'] + valid_var_names
                    widget_y_options = valid_var_names
                    widget_x = widgets.Dropdown(options=widget_x_options, value=widget_x_options[0], description='X:')
                    widget_y = widgets.Dropdown(options=widget_y_options, value=widget_y_options[0], description='Y:')

                    def on_widget_x_change(change):
                        x_name = widget_x.value
                        if x_name == 'index':
                            widget_y.options = valid_var_names
                        else:
                            widget_y.options = sorted(self.dim_names_to_var_names[self.ds[x_name].dimensions])
                        widget_y.value = widget_y.options[0]

                    widget_x.observe(on_widget_x_change, names='value')
                    interact(self._plot_1d_vars, x_name=widget_x, y_name=widget_y)

            else:
                raise ValueError('x_name and y_name must be given')
        else:
            self._plot_1d_vars(x_name, y_name)

    # TODO - remove
    def _plot_1d_vars(self, x_name, y_name):
        y_var = self.ds[y_name]
        y_units = y_var.units if hasattr(y_var, 'units') else '?'
        y_data = y_var[:]
        if x_name == 'index':
            x_units = '-'
            x_data = np.arange(0, len(y_data))
        else:
            x_var = self.ds[x_name]
            x_units = x_var.units if hasattr(x_var, 'units') else '?'
            x_data = x_var[:]

        plt.figure(figsize=(12, 6))
        plt.plot(x_data, y_data, 'b-')
        plt.xlabel('%s (%s)' % (x_name, x_units))
        plt.ylabel('%s (%s)' % (y_name, y_units))
        # ax.set_title('%s over %s' % (x_name, y_name))
        plt.grid(True)
        if self.interactive:
            plt.show()
        else:
            plt.savefig('%s_over_%s.png' % (x_name, y_name))

    def plot_im(self, name=None, vmin=None, vmax=None):
        if name is None:
            if self.interactive:
                name_options = list()
                for dim_names, var_names in self.dim_names_to_var_names.items():
                    no_zero_dim = all([self.dim_name_to_size[dim] > 0 for dim in dim_names])
                    if no_zero_dim and len(dim_names) == 2:
                        name_options.extend(var_names)
                name_options = sorted(name_options)
                # TODO (forman, 20160709): add sliders for vmin, vmax
                interact(self._plot_im, name=name_options, vmin=fixed(vmax), vmax=fixed(vmax))
            else:
                raise ValueError('name must be given')
        else:
            self._plot_im(name=name, vmin=vmin, vmax=vmax)

    def _plot_im(self, name, vmin=None, vmax=None):
        if name not in self.ds.variables:
            print('Error: "%s" is not a variable' % name)
            return
        var = self.ds[name]
        if len(var.shape) != 2:
            print('Error: "%s" is not 2-dimensional' % name)
            return
        var_data = var[:]

        vmin = vmin if vmin else var_data.min()
        vmax = vmax if vmax else var_data.max()
        plt.figure(figsize=(10, 10))
        plt.imshow(self.meas, interpolation='nearest', aspect='auto', vmin=vmin, vmax=vmax)
        # TODO (forman, 20160709): show labels in units of dimension variables
        plt.xlabel('%s (index)' % var.dimensions[1])
        plt.ylabel('%s (index)' % var.dimensions[0])
        plt.title('%s (%s)' % (name, var.units if hasattr(var, 'units') else '?'))
        plt.colorbar(orientation='vertical')
        if self.interactive:
            plt.show()
        else:
            plt.savefig('%s.png' % name)

    # TODO (forman, 20160709): replace ind, ref_ind by values in the 3rd-dimension's units
    def plot_2d3d_vars(self, x_name=None, y_name=None, ind=None, ref_ind=None):
        if not x_name or not y_name:
            if self.interactive:
                valid_dim_names = sorted([name for name, size in self.dim_name_to_size.items() if size > 0])

                widget_x_options = []
                widget_y_options = []
                for dim_names, var_names in self.dim_names_to_var_names.items():
                    if len(dim_names) == 1 and dim_names[0] in valid_dim_names:
                        widget_x_options.extend(var_names)
                    if len(dim_names) in {1, 2} and all([name in valid_dim_names for name in dim_names]):
                        widget_y_options.extend(var_names)

                widget_x_options = ['index'] + sorted(widget_x_options)
                widget_y_options = sorted(widget_y_options)

                widget_x = widgets.Dropdown(options=widget_x_options, value=widget_x_options[0], description='X:')
                widget_y = widgets.Dropdown(options=widget_y_options, value=widget_y_options[0], description='Y:')
                widget_z = widgets.IntSlider(value=0, min=0, max=100, step=1, description='Z:')

                def on_y_value_change(change):
                    print(change['new'])

                widget_y.observe(on_y_value_change, names='value')

                interact(self._plot_2d3d_vars, x_name=widget_x_options, y_name=widget_y_options, ref_ind=fixed(ref_ind))
            else:
                raise ValueError('x_name and y_name must be given')
        else:
            self._plot_2d3d_vars(x_name, y_name, ind, ref_ind)

    def _plot_2d3d_vars(self, x_name, y_name, ind, ref_ind):
        y_var = self.ds[y_name]
        y_units = y_var.units if hasattr(y_var, 'units') else '?'
        y_data = y_var[:]
        if x_name == 'index':
            x_units = '-'
            x_data = np.arange(0, len(y_data))
        else:
            x_var = self.ds[x_name]
            x_units = x_var.units if hasattr(x_var, 'units') else '?'
            x_data = x_var[:]

        plt.figure(figsize=(12, 6))
        plt.plot(x_data, y_data, 'b-')
        plt.xlabel('%s (%s)' % (x_name, x_units))
        plt.ylabel('%s (%s)' % (y_name, y_units))
        # ax.set_title('%s over %s' % (x_name, y_name))
        plt.grid(True)
        if self.interactive:
            plt.show()
        else:
            plt.savefig('%s_over_%s.png' % (x_name, y_name))


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    an = L1bAnalysis(args[0], interactive=False)
    an.plot_locs()
    an.plot_meas_im()
    an.plot_meas(ind=0)
    an.plot_meas(ind=2)
    an.plot_meas(ind=101, ref_ind=100)
    an.plot_meas_hist(vmax=1e7)
    an.plot_1d_vars('index', 'surf_type_l1b_echo_sar_ku')
    an.plot_1d_vars('lon_l1b_echo_sar_ku', 'lat_l1b_echo_sar_ku')

    # an.plot_meas(an.ds[''])


if __name__ == '__main__':
    main()
