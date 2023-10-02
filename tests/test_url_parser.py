from flinumeratr.url_parser import parse_flickr_url


def test_parses_a_single_image_url():
    url = 'https://www.flickr.com/photos/coast_guard/32812033543'
    
    assert parse_flickr_url(url) == {
        'type': 'single_image',
        'url': url,
        'photo_id': photo_id,
    }
