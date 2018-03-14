from unittest import TestCase

from dedop.model.exception import ProcessorException


class ProcessorExceptionTest(TestCase):
    def test_message_must_be_given(self):
        with self.assertRaises(ValueError) as e:
            ProcessorException(None)
        self.assertEqual(str(e.exception), 'message must be given')

        with self.assertRaises(ValueError) as e:
            ProcessorException('')
        self.assertEqual(str(e.exception), 'message must be given')

    def test_str(self):
        e = ProcessorException('bad L1A')
        self.assertEqual(str(e), 'bad L1A')

        e = ProcessorException(753)
        self.assertEqual(str(e), '753')
