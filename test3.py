import unittest
import os
from app import create_app




def test1():
    app = create_app()
    id = app.get_artist_id('beck')



if __name__ == '__main__':
    test1()