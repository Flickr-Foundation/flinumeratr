from flask.testing import FlaskClient
from flickr_photos_api import FlickrApi
import pytest


def test_can_load_homepage(client: FlaskClient) -> None:
    resp = client.get("/")

    assert resp.status_code == 200


def test_no_flickr_url_redirects_you_to_homepage(client: FlaskClient) -> None:
    resp = client.get("/see_photos")

    assert resp.status_code == 302
    assert resp.headers["location"] == "/"


def test_no_photos_to_show_is_error(client: FlaskClient) -> None:
    resp = client.get("/see_photos?flickr_url=https://www.flickr.com/help")

    assert resp.status_code == 200
    assert b"There are no photos to show" in resp.data


def test_not_a_flickr_url_is_error(client: FlaskClient) -> None:
    resp = client.get("/see_photos?flickr_url=https://www.example.net")

    assert resp.status_code == 200
    assert "doesn’t live on Flickr.com" in resp.data.decode("utf8")


@pytest.mark.parametrize(
    ["flickr_url", "expected_text"],
    [
        pytest.param(
            "https://www.flickr.com/photos/sdasmarchives/50567413447",
            [b"This URL is", b"a single photo"],
            id="single_photo",
        ),
        pytest.param(
            "https://www.flickr.com/photos/aljazeeraenglish/albums/72157626164453131",
            [
                b"This URL shows the photos in the",
                b"Faces from the Libyan front",
                b"album, which was created by",
                b"Al Jazeera English",
                b"It contains 22 photos",
            ],
            id="album",
        ),
        pytest.param(
            "https://www.flickr.com/groups/birdguide/",
            [
                b"This URL shows the photos in the",
                b"Field Guide: Birds of the World",
                b"group pool, which contains",
            ],
            id="group",
        ),
        pytest.param(
            "https://www.flickr.com/people/blueminds/",
            [
                b"This URL shows the photos taken by",
                b"Alexander Lauterbach",
                b"who has posted 370 photos",
            ],
            id="user",
        ),
        pytest.param(
            "https://www.flickr.com/photos/george/galleries/72157621848008117/",
            [
                b"This URL shows the photos in the",
                b"Photographs I Like of People I Don't Know",
                b"gallery",
                b"which contains 12 photos",
            ],
            id="gallery",
        ),
        pytest.param(
            "https://flickr.com/photos/tags/thatch/",
            [b"This URL shows photos tagged with", b"thatch"],
            id="tag",
        ),
    ],
)
def test_results_page_shows_info_box(
    client: FlaskClient, api: FlickrApi, flickr_url: str, expected_text: str
) -> None:
    resp = client.get(f"/see_photos?flickr_url={flickr_url}")

    assert resp.status_code == 200

    for text in expected_text:
        assert text in resp.data.replace(b"&nbsp;", b" ").replace(b"&#39;", b"'")


def test_can_load_small_photos_with_downloads_disabled(
    client: FlaskClient, api: FlickrApi
) -> None:
    # This is a URL that caused a 500 issue in prod -- the user only
    # has small photos, so we can't load the "Medium" photo size, but
    # they also have downloads disabled so we can't fall back to the
    # "Original" size when it's missing.
    resp = client.get(
        "/see_photos?flickr_url=https://www.flickr.com/people/25653675@N00/"
    )

    assert resp.status_code == 200


def test_cant_find_resource_is_error(client: FlaskClient, api: FlickrApi) -> None:
    resp = client.get(
        "/see_photos?flickr_url=https://www.flickr.com/photos/doesnotexist/12345678901234567890"
    )

    assert resp.status_code == 200
    assert b"Unable to find" in resp.data


def test_it_doesnt_show_date_taken_if_not_known(
    client: FlaskClient, api: FlickrApi
) -> None:
    resp = client.get(
        "/see_photos?flickr_url=https://www.flickr.com/photos/sdasmarchives/50567413447"
    )

    assert resp.status_code == 200
    assert b"taken None" not in resp.data


def test_empty_url_redirects_to_homepage(client: FlaskClient) -> None:
    resp = client.get("/see_photos?flickr_url=")

    assert resp.status_code == 302
    assert resp.headers["location"] == "/"
