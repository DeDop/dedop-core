

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