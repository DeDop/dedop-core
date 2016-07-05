from abc import ABCMeta, abstractmethod

from dedop.util.monitor import Monitor


class ProcessorException(Exception):
    """
    An exception type raised by :py:class:`BaseProcessor` and its derived classes.
    :param message: The exception message
    :param cause: Another error/exception that caused this one to be raised.
    """

    def __init__(self, message, cause=None):
        if not message:
            raise ValueError('message must be given')
        self.message = message
        self.cause = cause

    def __str__(self):
        return str(self.message)


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
