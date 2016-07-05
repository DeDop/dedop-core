import os.path
import time

from dedop.util.monitor import Monitor
from dedop.model.processor import BaseProcessor


class Processor(BaseProcessor):
    def __init__(self, config_name=None, chd_file=None, cnf_file=None, cst_file=None, skip_l1bs=False, output_dir=None):
        self.config_name = config_name
        self.chd_file = chd_file
        self.cnf_file = cnf_file
        self.cst_file = cst_file
        self.skip_l1bs = skip_l1bs
        self.output_dir = output_dir

    def process(self, l1a_file:str, monitor:Monitor=Monitor.NULL) -> int:
        os.makedirs(self.output_dir, exist_ok=True)
        with monitor.starting('Running DDP'):
            status = self._process_source(monitor.child(1), l1a_file)
            if status:
                return status
        return None

    # noinspection PyMethodMayBeStatic
    def _process_source(self, monitor: Monitor, l1a_file: str) -> int:
        # to simulate an error
        if l1a_file == 'e':
            return 1, 'I/O Error: Failed to open L1A file %s' % l1a_file
        num_recs = 100
        total_work = num_recs
        if not self.skip_l1bs:
            total_work += 1
        total_work += 1
        with monitor.starting('Processing L1A ' + l1a_file, total_work):
            for rec in range(num_recs):
                if monitor.is_cancelled():
                    return -1, 'Processing cancelled by user'
                # simulate some processing
                time.sleep(1.0 / num_recs)
                monitor.progress(1)

            l1a_base, _ = os.path.splitext(os.path.basename(l1a_file))
            if l1a_base.startswith('L1A'):
                l1a_base = l1a_base[len('L1A'):]

            if not self.skip_l1bs:
                l1bs_name = 'L1BS_%s_%s.nc' % (l1a_base, self.config_name)
                with open(os.path.join(self.output_dir, l1bs_name), 'wb'):
                    monitor.progress(1, msg="Writing %s ..." % l1bs_name)

            l1b_name = 'L1B_%s_%s.nc' % (l1a_base, self.config_name)
            with open(os.path.join(self.output_dir, l1b_name), 'wb'):
                monitor.progress(1, msg="Writing %s ..." % l1b_name)

        return None
