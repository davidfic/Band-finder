#!flask/bin/python
import os
import unittest

from app import create_app
class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

    def tearDown(self):
        pass

    def test_avatar(self):
        assert 2 == 2

if __name__ == '__main__':
    unittest.main()
