import pytest

from flinumeratr.enumerator import categorise_flickr_url, NotAFlickrUrl


@pytest.mark.parametrize(
    "url",
    [
        "" "1.2.3.4",
        "https://example.net",
        "ftp://s3.amazonaws.com/my-bukkit/object.txt",
        "http://http://",
    ],
)
def test_it_rejects_a_url_which_isnt_flickr(url):
    with pytest.raises(NotAFlickrUrl):
        categorise_flickr_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/photos/coast_guard/32812033543",
        "http://www.flickr.com/photos/coast_guard/32812033543",
        "https://flickr.com/photos/coast_guard/32812033543",
        "http://flickr.com/photos/coast_guard/32812033543",
        "www.flickr.com/photos/coast_guard/32812033543",
        "flickr.com/photos/coast_guard/32812033543",
    ],
)
def test_it_can_categorise_urls_even_if_the_host_is_a_bit_unusual(url):
    assert categorise_flickr_url(url) == {
        "type": "single_photo",
        "photo_id": "32812033543",
    }


@pytest.mark.parametrize(
    ["url", "photo_id"],
    [
        ("https://www.flickr.com/photos/coast_guard/32812033543", "32812033543"),
        (
            "https://www.flickr.com/photos/coast_guard/32812033543/in/photolist-RZufqg-ebEcP7-YvCkaU-2dKrfhV-6o5anp-7ZjJuj-fxZTiu-2c1pGwi-JbqooJ-TaNkv5-ehrqn7-2aYFaRh-QLDxJX-2dKrdip-JB7iUz-ehrsNh-2aohZ14-Rgeuo3-JRwKwE-ksAR6U-dZVQ3m-291gkvk-26ynYWn-pHMQyE-a86UD8-9Tpmru-hamg6T-8ZCRFU-QY8amt-2eARQfP-qskFkD-2c1pG1Z-jbCpyF-fTBQDa-a89xfd-a7kYMs-dYjL51-5XJgXY-8caHdL-a89HZd-9GBmft-xy7PBo-sai77d-Vs8YPG-RgevC7-Nv5CF6-e4ZLn9-cPaxqS-9rnjS9-8Y7mhm",
            "32812033543",
        ),
        (
            "https://www.flickr.com/photos/britishlibrary/13874001214/in/album-72157644007437024/",
            "13874001214",
        ),
    ],
)
def test_it_categorises_a_single_photo(url, photo_id):
    assert categorise_flickr_url(url) == {
        "type": "single_photo",
        "photo_id": photo_id,
    }


def test_it_categories_an_album():
    url = "https://www.flickr.com/photos/cat_tac/albums/72157666833379009"

    assert categorise_flickr_url(url) == {
        "type": "photoset",
        "user_url": "https://www.flickr.com/photos/cat_tac",
        "photoset_id": "72157666833379009",
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/photos/blueminds/",
        "https://www.flickr.com/people/blueminds/",
        "https://www.flickr.com/photos/blueminds/albums",
        "https://www.flickr.com/photos/blueminds/page3",
    ],
)
def test_it_categorises_a_person(url):
    assert categorise_flickr_url(url) == {
        "type": "people",
        "user_url": "https://www.flickr.com/photos/blueminds",
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/groups/slovenia/pool/",
        "https://www.flickr.com/groups/slovenia/",
        "https://www.flickr.com/groups/slovenia/pool/page30",
    ],
)
def test_it_categorises_a_group(url):
    assert categorise_flickr_url(url) == {
        "type": "group",
        "group_url": "https://www.flickr.com/groups/slovenia",
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/photos/flickr/galleries/72157722096057728/",
        "https://www.flickr.com/photos/flickr/galleries/72157722096057728/page2",
    ],
)
def test_it_categorises_a_gallery(url):
    assert categorise_flickr_url(url) == {
        "type": "galleries",
        "gallery_id": "72157722096057728",
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://flickr.com/photos/tags/fluorspar/",
        "https://flickr.com/photos/tags/fluorspar/page1",
    ],
)
def test_it_categories_a_tag(url):
    assert categorise_flickr_url(url) == {
        "type": "tags",
        "tag": "fluorspar",
    }
