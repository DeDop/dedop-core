from contextlib import contextmanager

import sys
from io import StringIO


@contextmanager
def fetch_std_streams():
    """
    A context manager which can be used to temporarily fetch the standard output streams
    ``sys.stdout`` and  ``sys.stderr``.

    Usage:::

        with fetch_std_streams() as stdout, stderr
            sys.stdout.write('yes')
            sys.stderr.write('oh no')
        print('fetched', stdout.getvalue())
        print('fetched', stderr.getvalue())

    :return: yields ``sys.stdout`` and  ``sys.stderr`` redirected into buffers of type ``StringIO``
    """
    sys.stdout.flush()
    sys.stderr.flush()

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = StringIO()
    sys.stderr = StringIO()

    try:
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout.flush()
        sys.stderr.flush()

        sys.stdout = old_stdout
        sys.stderr = old_stderr
