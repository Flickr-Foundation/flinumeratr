import os
from typing import Generator

from flask.testing import FlaskClient
import pytest
from pytest import FixtureRequest
import vcr

from flickr_photos_api import FlickrPhotosApi


@pytest.fixture
def user_agent() -> str:
    return "flinumeratr/dev (https://github.com/Flickr-Foundation/flinumeratr; hello@flickr.org)"


@pytest.fixture(scope="function")
def cassette_name(request: FixtureRequest) -> str:
    """
    Returns the name of a cassette for vcr.py.

    The name is made up of two parts:

    -   the name of the test function
    -   the ID of the test case in @pytest.mark.parametrize

    """
    name_parts = []

    # Add the name of the test function.
    #
    # See https://stackoverflow.com/a/67056955/1558022 for more info
    # on how this works.
    function_name = request.function.__name__
    name_parts.append(function_name)

    # Finally, add the name of the test case in @pytest.mark.parametrize,
    # if there is one.
    try:
        name_parts.append(request.node.callspec.id)
    except AttributeError:  # not in a parametrised test
        pass

    return ".".join(name_parts) + ".yml"


@pytest.fixture(scope="function")
def api(cassette_name: str, user_agent: str) -> Generator[FlickrPhotosApi, None, None]:
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
        yield FlickrPhotosApi(
            api_key=os.environ.get("FLICKR_API_KEY", "<REDACTED>"),
            user_agent=user_agent,
        )


@pytest.fixture()
def client() -> Generator[FlaskClient, None, None]:
    """
    Creates an instance of the app for use in testing.

    See https://flask.palletsprojects.com/en/3.0.x/testing/#fixtures
    """
    from flinumeratr.app import app

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
