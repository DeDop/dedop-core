import sys

import matplotlib.pyplot as plt
import numpy as np
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

    @property
    def attribs(self):
        return {name: self.ds.getncattr(name) for name in self.ds.ncattrs()}

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


if __name__ == '__main__':
    main()
