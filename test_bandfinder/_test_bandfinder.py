import os
import unittest
from app.init import create_app
import pytest

@pytest.fixture
def test_anything():
    print('fuck you')

class BandfinderTestCase(unittest.TestCast):

    def setUp(self):
        self.app = app.create_app()

    def test_artist_id(self):
        app = create_app()
        artist_id = app.get_artist_id('beck')
        assert artist_id == '3vbKDsSS70ZX9D2OcvbZmS'
