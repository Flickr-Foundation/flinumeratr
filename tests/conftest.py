from collections.abc import Iterator
import os

from flask.testing import FlaskClient
from flickr_photos_api import FlickrApi
from nitrate.cassettes import cassette_name
import pytest
import vcr


@pytest.fixture
def user_agent() -> str:
    return "flinumeratr/dev (https://github.com/Flickr-Foundation/flinumeratr; hello@flickr.org)"


@pytest.fixture(scope="function")
def api(cassette_name: str, user_agent: str) -> Iterator[FlickrApi]:
    """
    Creates an instance of the FlickrPhotosApi class for use in tests.

    This instance of the API will record its interactions as "cassettes"
    using vcr.py, which can be replayed offline (e.g. in CI tests).
    """
    with vcr.use_cassette(
        cassette_name,
        cassette_library_dir="tests/fixtures/cassettes",
        filter_query_parameters=["api_key"],
    ):
        yield FlickrApi.with_api_key(
            api_key=os.environ.get("FLICKR_API_KEY", "<REDACTED>"),
            user_agent=user_agent,
        )


@pytest.fixture()
def client() -> Iterator[FlaskClient]:
    """
    Creates an instance of the app for use in testing.

    See https://flask.palletsprojects.com/en/3.0.x/testing/#fixtures
    """
    os.environ.setdefault("FLICKR_API_KEY", "<testing>")

    from flinumeratr.app import app

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


__all__ = ["cassette_name", "user_agent", "api", "client"]
