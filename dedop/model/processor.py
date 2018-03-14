import os.path
import time
from abc import ABCMeta, abstractmethod

from dedop.util.monitor import Monitor


class BaseProcessor(metaclass=ABCMeta):
    """
    Defines a common interface for all processor objects.
    """

    @abstractmethod
    def process(self, l1a_file: str, monitor: Monitor = Monitor.NULL):
        """
        Run the processor on the provided L1A product given by *l1a_file*.
        Processing progress may be reported through the given *monitor*.

        :param l1a_file: The L1A file path.
        :param monitor: A progress monitor.
        :raises ProcessorException: if any error occurs.
        """


class DummyProcessor(BaseProcessor):
    """
    Create a new dummy processor instance useful for testing.

    :param name: the processor "run" name, will be used to name L1B, L1BS output files
    :param cnf_file: configuration definition file
    :param cst_file: constants definition file
    :param chd_file: characterisation definition file
    :param output_dir: the output directory for L1B, L1BS, and log-files, etc.
    :param skip_l1bs: whether to skip L1BS output
    :return: an object of type :py_class:`BaseProcessor`
    """

    def __init__(self,
                 name=None,
                 cnf_file=None,
                 cst_file=None,
                 chd_file=None,
                 output_dir=None,
                 skip_l1bs=False):
        self.name = name
        self.cnf_file = cnf_file
        self.cst_file = cst_file
        self.chd_file = chd_file
        self.output_dir = output_dir
        self.skip_l1bs = skip_l1bs

    def process(self, l1a_file: str, monitor: Monitor = Monitor.NULL):
        """
        Simulate processing a single L1A to L1B and L1BS.

        :param l1a_file: Path to L1A file.
        :param monitor: Progress monitor.
        :raises ProcessorException: if the string 'ERR' occurs in the *l1a_file* filename
        """
        if 'ERR' in os.path.basename(l1a_file).upper():
            raise ProcessorException('failed to open L1A file %s' % l1a_file)

        num_recs = 100
        total_work = num_recs
        if not self.skip_l1bs:
            total_work += 1
        total_work += 1

        with monitor.starting('processing "%s"' % self.name, total_work=total_work):
            for rec in range(num_recs):
                if monitor.is_cancelled():
                    return
                # simulate some processing
                time.sleep(1.0 / num_recs)
                monitor.progress(work=1)

            os.makedirs(self.output_dir, exist_ok=True)

            l1a_base, _ = os.path.splitext(os.path.basename(l1a_file))
            if l1a_base.startswith('L1A'):
                l1a_base = l1a_base[len('L1A'):]

            if not self.skip_l1bs:
                l1bs_name = 'L1BS_%s_%s.nc' % (l1a_base, self.name)
                with open(os.path.join(self.output_dir, l1bs_name), 'wb'):
                    monitor.progress(work=1, msg='writing L1BS')

            l1b_name = 'L1B_%s_%s.nc' % (l1a_base, self.name)
            with open(os.path.join(self.output_dir, l1b_name), 'wb'):
                monitor.progress(work=1, msg='writing L1B')
