import os
from typing import Generator

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

    The name can be made up of (up to) three parts:

    -   the name of the test class
    -   the name of the test function
    -   the ID of the test case in @pytest.mark.parametrize

    """
    name_parts = []

    # The node ID gives us the relative path to the test file, the
    # class name (if running in a class), and the function name.
    #
    # Prepend cassettes with their class name -- this avoids tests
    # with the same function name in different classes from getting
    # overlapping cassettes.
    #
    # Examples of request.node.nodeid:
    #
    #     tests/test_api.py::test_it_throws_if_bad_auth
    #     tests/test_api.py::test_lookup_user_by_url[obamawhitehouse]
    #
    # See https://stackoverflow.com/a/68804077/1558022
    node_id = request.node.nodeid.split("::")
    if len(node_id) == 3:
        test_class_name = node_id[1]
        name_parts.append(test_class_name)

    # Then add the name of the test function.
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
def vcr_cassette(cassette_name: str) -> Generator[None, None, None]:
    """
    Creates a VCR cassette for use in tests.

    Anything using httpx in this test will record its HTTP interactions
    as "cassettes" using vcr.py, which can be replayed offline
    (e.g. in CI tests).
    """
    with vcr.use_cassette(
        cassette_name,
        cassette_library_dir="tests/fixtures/cassettes",
    ):
        yield


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
def client():
    """
    Creates an instance of the app for use in testing.

    See https://flask.palletsprojects.com/en/3.0.x/testing/#fixtures
    """
    if "FLICKR_API_KEY" not in os.environ:
        os.environ["FLICKR_API_KEY"] = "testing"

    from flinumeratr.app import app

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
