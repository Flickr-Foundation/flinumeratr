import pytest


def test_no_flickr_url_redirects_you_to_homepage(client):
    resp = client.get("/see_photos")

    assert resp.status_code == 302
    assert resp.headers['location'] == '/'


@pytest.mark.parametrize(
    ["flickr_url", "expected_text"],
    [
        (
            "https://www.flickr.com/photos/sdasmarchives/50567413447",
            [b"This URL is", b"a single photo"],
        ),
        (
            "https://www.flickr.com/photos/aljazeeraenglish/albums/72157626164453131",
            [
                b"This URL shows the photos in the",
                b"Faces from the Libyan front",
                b"album, which was created by",
                b"Al Jazeera English",
                b"It contains 22 photos",
            ],
        ),
        (
            "https://www.flickr.com/groups/birdguide/",
            [
                b"This URL shows the photos in the",
                b"Field Guide: Birds of the World",
                b"group pool, which contains 211,457 photos",
            ],
        ),
        (
            "https://www.flickr.com/people/blueminds/",
            [
                b"This URL shows the photos taken by",
                b"Alexander Lauterbach",
                b"who has posted 365 photos",
            ],
        ),
        (
            "https://www.flickr.com/photos/george/galleries/72157621848008117/",
            [
                b"This URL shows the photos in the",
                b"Photographs I Like of People I Don't Know",
                b"gallery",
                b"which contains 13 photos",
            ],
        ),
        (
        "https://flickr.com/photos/tags/thatch/",
        [
            b"This URL shows photos tagged with",
            b"thatch"
        ]
        )
    ],
)
def test_results_page_shows_info_box(client, api, flickr_url, expected_text):
    resp = client.get(f"/see_photos?flickr_url={flickr_url}")

    assert resp.status_code == 200

    for text in expected_text:
        assert text in resp.data.replace(b"&nbsp;", b" ").replace(b"&#39;", b"'")
