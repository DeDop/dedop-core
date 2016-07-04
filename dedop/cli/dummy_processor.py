import os.path
import time

from dedop.util.monitor import Monitor


# TODO (forman, 20160616) - implement the true processor interface

class Processor:
    def __init__(self, config_name=None, chd_file=None, cnf_file=None, cst_file=None, skip_l1bs=False, output_dir=None):
        self.config_name = config_name
        self.chd_file = chd_file
        self.cnf_file = cnf_file
        self.cst_file = cst_file
        self.skip_l1bs = skip_l1bs
        self.output_dir = output_dir

    def process_sources(self, monitor: Monitor, *l1a_files) -> int:
        os.makedirs(self.output_dir, exist_ok=True)
        with monitor.starting('Running DDP', len(l1a_files)):
            for l1a_file in l1a_files:
                status = self._process_source(monitor.child(1), l1a_file)
                if status:
                    return status
        return None

    # noinspection PyMethodMayBeStatic
    def _process_source(self, monitor: Monitor, l1a_file:str) -> int:
        # to simulate an error
        if l1a_file == 'e':
            return 1, 'I/O Error: Failed to open L1A file %s' % l1a_file
        num_recs = 1000
        with monitor.starting('Processing L1A ' + l1a_file, num_recs):
            for rec in range(num_recs):
                if monitor.is_cancelled():
                    return -1, 'Processing cancelled by user'
                # simulate some processing
                time.sleep(2.0 / num_recs)
                monitor.progress(1)

        l1a_filename = os.path.basename(l1a_file)
        l1a_base, _ = os.path.splitext(os.path.basename(l1a_file))
        if l1a_base.startswith('L1A'):
            l1a_base = l1a_base[len('L1A'):]

        if not self.skip_l1bs:
            l1bs_name = 'L1BS_%s_%s.nc' % (l1a_base, self.config_name)
            with open(os.path.join(self.output_dir, l1bs_name), 'wb'):
                print("Writing %s ..." % l1bs_name)

        l1b_name = 'L1B_%s_%s.nc' % (l1a_base, self.config_name)
        with open(os.path.join(self.output_dir, l1b_name), 'wb'):
            print("Writing L1B-%s.nc ..." % l1b_name)

        return None
