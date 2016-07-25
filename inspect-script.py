import sys

from dedop.ui.inspect import inspect_l1b_product

l1b_file = sys.argv[1]

l1b = inspect_l1b_product(l1b_file, interactive=False)

l1b.plot.locations()
l1b.plot.waveform_3d_surf()
l1b.plot.waveform_3d_poly()
l1b.plot.waveform_3d_line()
l1b.plot.waveform_im()
l1b.plot.waveform_line(ind=0)
l1b.plot.waveform_line(ind=2)
l1b.plot.waveform_line(ind=101, ref_ind=100)
l1b.plot.waveform_hist(vmax=1e7)

l1b.plot.im_line(z='i2q2_meas_ku_l1b_echo_sar_ku')
l1b.plot.im_line(z='i2q2_meas_ku_l1b_echo_sar_ku', xind=100)
l1b.plot.im_line(z='i2q2_meas_ku_l1b_echo_sar_ku', yind=100)
l1b.plot.im_line(z='i2q2_meas_ku_l1b_echo_sar_ku', xind=100, yind=100)
l1b.plot.line(x='index', y='surf_type_l1b_echo_sar_ku')
l1b.plot.line(x='lon_l1b_echo_sar_ku', y='lat_l1b_echo_sar_ku')
l1b.plot.im('i2q2_meas_ku_l1b_echo_sar_ku')

l1b.close()
