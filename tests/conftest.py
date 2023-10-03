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
    with vcr.use_cassette(
        request.function.__name__ + ".yml",
        cassette_library_dir="tests/fixtures/cassettes",
        filter_query_parameters=["api_key"],
        record_mode="once",
    ):
        yield FlickrApi(api_key=os.environ.get("FLICKR_API_KEY", "<REDACTED>"))
