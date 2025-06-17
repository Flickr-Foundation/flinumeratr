from collections.abc import Iterator
import os

from flask.testing import FlaskClient
from flickr_api import FlickrApi
from flickr_api.fixtures import flickr_api
from nitrate.cassettes import cassette_name
import pytest


__all__ = ["flickr_api", "client", "cassette_name"]


@pytest.fixture()
def client(flickr_api: FlickrApi) -> Iterator[FlaskClient]:
    """
    Creates an instance of the app for use in testing.

    See https://flask.palletsprojects.com/en/3.0.x/testing/#fixtures
    """
    os.environ.setdefault("FLICKR_API_KEY", "<testing>")

    from flinumeratr.app import app

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
