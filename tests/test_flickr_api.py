import os

import httpx
import pytest
import vcr

from flinumeratr.flickr_api import FlickrApi, get_single_photo_info


@pytest.fixture(scope='function')
def api(request):
    with vcr.use_cassette(
        request.function.__name__ + '.yml',
        cassette_library_dir='tests/fixtures/cassettes',
        filter_query_parameters=['api_key'],
        record_mode='once',
    ):
        yield FlickrApi(api_key=os.environ.get('FLICKR_API_KEY', '<REDACTED>'))


def test_get_single_photo_info(api):
    info = get_single_photo_info(api, photo_id='32812033543')
    assert info == {
        'title': 'Puppy Kisses'
    }
    