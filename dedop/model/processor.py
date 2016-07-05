from abc import ABCMeta, abstractmethod
from dedop.util.monitor import Monitor

class BaseProcessor(metaclass=ABCMeta):
    """
    defines interface from processor objects
    """

    @abstractmethod
    def process(self, l1a_file: str, monitor: Monitor=Monitor.NULL) -> int:
        """
        runs the processor on the provided L1A file. returns True if processing completes
        successfully, false otherwise.
        """