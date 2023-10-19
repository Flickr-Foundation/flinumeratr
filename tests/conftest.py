import os

import pytest
import vcr

from flinumeratr.flickr_api import FlickrApi


@pytest.fixture(scope="function")
def cassette_name(request):
    # By default we use the name of the test as the cassette name,
    # but if it's a test parametrised with @pytest.mark.parametrize,
    # we include the parameter name to distinguish cassettes.
    #
    # See https://stackoverflow.com/a/67056955/1558022 for more info
    # on how this works.
    try:
        fixture_name = request.node.callspec.id.replace("/", "-").replace(":", "-")
        return f"{request.function.__name__}.{fixture_name}.yml"
    except AttributeError:
        return f"{request.function.__name__}.yml"


@pytest.fixture(scope="function")
def api(cassette_name):
    """
    Creates an instance of the FlickrApi class for use in tests.

    This instance of the API will record its interactions as "cassettes"
    using vcr.py, which can be replayed offline (e.g. in CI tests).
    """
    with vcr.use_cassette(
        cassette_name,
        cassette_library_dir="tests/fixtures/cassettes",
        filter_query_parameters=["api_key"],
    ):
        yield FlickrApi(api_key=os.environ.get("FLICKR_API_KEY", "<REDACTED>"))
