import os
import tempfile

import pytest

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        """ If your fixture uses "yield" instead of "return", pytest understands
        that the post-yield code is for tearing down objects and connections. """
        yield client

    # Client tear-down actions go here


def test_homepage(client):
    """Make sure root returns 200"""

    rv = client.get("/")
    assert b'GET received' in rv.data
