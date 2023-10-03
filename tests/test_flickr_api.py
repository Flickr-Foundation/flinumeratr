import os

import httpx
import vcr

from flinumeratr.flickr_api import FlickrApi, get_single_photo_info


@vcr.use_cassette(
    cassette_library_dir='tests/fixtures/cassettes',
    filter_query_parameters=['api_key'],
    record_mode='once',
)
def test_get_single_photo_info():
    api = FlickrApi(api_key=os.environ.get('FLICKR_API_KEY', '<REDACTED>'))
    client = httpx.Client(
    base_url=api.client.base_url,
    params=api.client.params)
    api.client = client
    
    info = get_single_photo_info(api, photo_id='32812033543')
    assert info == {
        'title': 'Puppy Kisses'
    }
    