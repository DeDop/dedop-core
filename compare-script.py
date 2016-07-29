import sys

from dedop.ui.compare import compare_l1b_products

l1b_file_1 = sys.argv[1]
l1b_file_2 = sys.argv[2]

comp = compare_l1b_products(l1b_file_1, l1b_file_2, output_path='./comp-test')
#comp = compare_l1b_products(l1b_file_1, l1b_file_2, output_path='./comp-test.pdf')

comp.plot.locations()
comp.p1.plot.waveform_im()
comp.p2.plot.waveform_im()
comp.plot.waveforms_delta_im()
comp.plot.waveforms_hist()
comp.plot.waveforms_delta_hist()
comp.plot.waveforms_hexbin()
comp.plot.waveforms_scatter()

comp.close()
