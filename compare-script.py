import sys

from dedop.ui.compare import compare_l1b_products

###############################################################################
# Simple command-line parsing

prog = sys.argv[0]
args = sys.argv[1:]

if len(args) not in [3, 4]:
    print('usage: %s L1B_FILE_1 L1B_FILE_2 OUT_FILE [FORMAT]' % prog)
    print('       with FORMAT being "png" or "dir"')
    exit(1)

l1b_file_1 = args[0]
l1b_file_2 = args[1]
out_file = args[2]
out_format = args[3] if len(args) == 4 else None

###############################################################################
# The actual analysis

comp = compare_l1b_products(l1b_file_1, l1b_file_2, output_path=out_file, output_format=out_format)

comp.plot.locations()
comp.p1.plot.waveform_im()
comp.p2.plot.waveform_im()
comp.plot.waveforms_delta_im()
comp.plot.waveforms_hist()
comp.plot.waveforms_delta_hist()
comp.plot.waveforms_hexbin()
comp.plot.waveforms_scatter()

# Perform any other analysis here using the data members of 'comp', 'comp.p1', and 'comp.p2'.

comp.close()

#
###############################################################################
