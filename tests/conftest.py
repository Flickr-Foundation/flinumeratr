import os

import pytest
import vcr

from flinumeratr.flickr_api import FlickrApi


@pytest.fixture(scope="function")
def api(request):
    """
    Creates an instance of the FlickrApi class for use in tests.

    This instance of the API will record its interactions as "cassettes"
    using vcr.py, which can be replayed offline (e.g. in CI tests).
    """
    # By default we use the name of the test as the cassette name,
    # but if it's a test parametrised with @pytest.mark.parametrize,
    # we include the parameter name to distinguish cassettes.
    #
    # See https://stackoverflow.com/a/67056955/1558022 for more info
    # on how this works.
    try:
        cassette_name = f"{request.function.__name__}.{request.node.callspec.id}.yml"
    except AttributeError:
        cassette_name = f"{request.function.__name__}.yml"

    with vcr.use_cassette(
        cassette_name,
        cassette_library_dir="tests/fixtures/cassettes",
        filter_query_parameters=["api_key"],
        record_mode="once",
    ):
        yield FlickrApi(api_key=os.environ.get("FLICKR_API_KEY", "<REDACTED>"))
