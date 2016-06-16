import sys
from contextlib import contextmanager
from io import StringIO
from unittest import TestCase

from dedop import cli


@contextmanager
def fetch_std_streams():
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


class CliMainTest(TestCase):
    def test_noargs(self):
        with self.assertRaises(SystemExit):
            cli.main()

    def test_command_run_help(self):
        with self.assertRaises(SystemExit):
            cli.main(args=['run', '-h'])

        with self.assertRaises(SystemExit):
            cli.main(args=['run', '-help'])

    def test_invalid_command(self):
        with self.assertRaises(SystemExit):
            cli.main(['pipo'])

    def test_option_help(self):
        with self.assertRaises(SystemExit):
            cli.main(args=['--h'])
        with self.assertRaises(SystemExit):
            cli.main(args=['--help'])

    def test_option_version(self):
        with self.assertRaises(SystemExit):
            cli.main(args=['--version'])

    def test_command_license(self):
        with fetch_std_streams() as (sout, serr):
            status = cli.main(args=['license'])
            self.assertEqual(status, 0)
        self.assertIn('GNU GENERAL PUBLIC LICENSE', sout.getvalue())
        self.assertEqual(serr.getvalue(), '')

    def test_command_copyright(self):
        with fetch_std_streams() as (sout, serr):
            status = cli.main(args=['copyright'])
            self.assertEqual(status, 0)
        self.assertIn('European Space Agency', sout.getvalue())
        self.assertEqual(serr.getvalue(), '')
