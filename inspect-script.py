import sys

from dedop.ui.inspect import inspect_l1b_product

l1b_file = sys.argv[1]

insp = inspect_l1b_product(l1b_file, output_path='./inspect-test')
#insp = inspect_l1b_product(l1b_file, output_path='./inspect-test.pdf')

insp.plot.locations()
insp.plot.waveform_3d_surf()
insp.plot.waveform_3d_poly()
insp.plot.waveform_3d_line()
insp.plot.waveform_im()
insp.plot.waveform_line(ind=0)
insp.plot.waveform_line(ind=2)
insp.plot.waveform_line(ind=101, ref_ind=100)
insp.plot.waveform_hist(vmax=1e7)

insp.plot.im_line(z='i2q2_meas_ku_l1b_echo_sar_ku')
insp.plot.im_line(z='i2q2_meas_ku_l1b_echo_sar_ku', xind=100)
insp.plot.im_line(z='i2q2_meas_ku_l1b_echo_sar_ku', yind=100)
insp.plot.im_line(z='i2q2_meas_ku_l1b_echo_sar_ku', xind=100, yind=100)
insp.plot.line(x='index', y='surf_type_l1b_echo_sar_ku')
insp.plot.line(x='lon_l1b_echo_sar_ku', y='lat_l1b_echo_sar_ku')
insp.plot.im('i2q2_meas_ku_l1b_echo_sar_ku')

insp.close()
