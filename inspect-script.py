import sys

from dedop.ui.inspect import inspect_l1b_product

###############################################################################
# Simple command-line parsing

prog = sys.argv[0]
args = sys.argv[1:]

if len(args) not in [2, 3]:
    print('usage: %s L1B_FILE OUT_FILE [FORMAT]' % prog)
    print('       with FORMAT being "png" or "dir"')
    exit(1)

l1b_file = args[0]
out_file = args[1]
out_format = args[2] if len(args) == 3 else None

###############################################################################
# The actual analysis

insp = inspect_l1b_product(l1b_file, output_path=out_file, output_format=out_format)

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

# Perform any other analysis here using the data members of 'insp'.

insp.close()

#
###############################################################################
