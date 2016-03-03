import io
from unittest import TestCase
from minimocktest import MockTestCase

__author__ = 'wardcoessens'


class MockedTestCase(TestCase, MockTestCase):

    def _pre_setup(self):
        MockTestCase.setUp()
        TestCase.__pre_setup()

        def _post_teardown(self):
            TestCase._post_teardown(self)
            MockTestCase.tearDown()


class TestOrder(MockTestCase):
    def setUp(self):
        self.file = io.StringIO.StringIO('MiniMockTest')
        self.file.close = self.Mock('file_close_function')
    def test_get_url(self):