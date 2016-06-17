import time

from dedop.util.monitor import Monitor


# todo (nf, 20160616) - implement the true processor interface

class Processor:
    def __init__(self, name=None, config=None, skip_l1bs=False):
        self.skip_l1bs = skip_l1bs
        self.config = config
        self.name = name

    def process_sources(self, monitor: Monitor, *l1a_files) -> int:
        with monitor.starting('Running DDP', len(l1a_files)):
            for l1a_file in l1a_files:
                status = self.process_source(monitor.child(1), l1a_file)
                if status:
                    return status
        return None

    # noinspection PyMethodMayBeStatic
    def process_source(self, monitor, l1a_file) -> int:
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

        if not self.skip_l1bs:
            print("Writing L1BS-%s.nc ..." % self.name)
        print("Writing L1B-%s.nc ..." % self.name)
        return None
