import pytest

from flinumeratr.url_parser import categorise_flickr_url, NotAFlickrUrl


def test_it_rejects_a_url_which_isnt_flickr():
    with pytest.raises(NotAFlickrUrl):
        categorise_flickr_url('https://example.net')


def test_it_categorises_a_single_image():
    url = 'https://www.flickr.com/photos/coast_guard/32812033543'
    
    assert categorise_flickr_url(url) == {
        'type': 'single_image',
        'url': url,
        'photo_id': '32812033543',
    }


def test_it_categorises_a_single_image_in_a_photoset():
    url = 'https://www.flickr.com/photos/coast_guard/32812033543/in/photolist-RZufqg-ebEcP7-YvCkaU-2dKrfhV-6o5anp-7ZjJuj-fxZTiu-2c1pGwi-JbqooJ-TaNkv5-ehrqn7-2aYFaRh-QLDxJX-2dKrdip-JB7iUz-ehrsNh-2aohZ14-Rgeuo3-JRwKwE-ksAR6U-dZVQ3m-291gkvk-26ynYWn-pHMQyE-a86UD8-9Tpmru-hamg6T-8ZCRFU-QY8amt-2eARQfP-qskFkD-2c1pG1Z-jbCpyF-fTBQDa-a89xfd-a7kYMs-dYjL51-5XJgXY-8caHdL-a89HZd-9GBmft-xy7PBo-sai77d-Vs8YPG-RgevC7-Nv5CF6-e4ZLn9-cPaxqS-9rnjS9-8Y7mhm'
    
    assert categorise_flickr_url(url) == {
        'type': 'single_image',
        'url': url,
        'photo_id': '32812033543',
    }
