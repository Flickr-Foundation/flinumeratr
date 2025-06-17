from flask.testing import FlaskClient
from flickr_api import FlickrApi
import pytest


def test_load_homepage(client: FlaskClient) -> None:
    """
    Load the Flinumeratr homepage.
    """
    resp = client.get("/")

    assert resp.status_code == 200


def test_no_flickr_url_redirects_you_to_homepage(client: FlaskClient) -> None:
    """
    If you load /see_photos without passing a URL, you're redirected
    to the homepage.
    """
    resp = client.get("/see_photos")

    assert resp.status_code == 302
    assert resp.headers["location"] == "/"


def test_no_photos_to_show_is_error(client: FlaskClient) -> None:
    """
    If you look up a URL which doesn't have any photos, you get
    a helpful error.
    """
    resp = client.get("/see_photos?flickr_url=https://www.flickr.com/help")

    assert resp.status_code == 200
    assert "There are no photos to show" in resp.text


def test_not_a_flickr_url_is_error(client: FlaskClient) -> None:
    """
    If you look up a URL which isn't on Flickr.com, you get a helpful error.
    """
    resp = client.get("/see_photos?flickr_url=https://www.example.net")

    assert resp.status_code == 200
    assert "doesn’t live on Flickr.com" in resp.text


@pytest.mark.parametrize(
    ["flickr_url", "expected_text"],
    [
        pytest.param(
            "https://www.flickr.com/photos/sdasmarchives/50567413447",
            ["This URL is", "a single photo"],
            id="single_photo",
        ),
        pytest.param(
            "https://www.flickr.com/photos/aljazeeraenglish/albums/72157626164453131",
            [
                "This URL shows the photos in the",
                "Faces from the Libyan front",
                "album, which was created by",
                "Al Jazeera English",
                "It contains 22 photos",
            ],
            id="album",
        ),
        pytest.param(
            "https://www.flickr.com/groups/birdguide/",
            [
                "This URL shows the photos in the",
                "Field Guide: Birds of the World",
                "group pool, which contains",
            ],
            id="group",
        ),
        pytest.param(
            "https://www.flickr.com/people/blueminds/",
            [
                "This URL shows the photos taken by",
                "Alexander Lauterbach",
                "who has posted 375 photos",
            ],
            id="user",
        ),
        pytest.param(
            "https://www.flickr.com/photos/george/galleries/72157621848008117/",
            [
                "This URL shows the photos in the",
                "Photographs I Like of People I Don't Know",
                "gallery",
                "which contains 13 photos",
            ],
            id="gallery",
        ),
        pytest.param(
            "https://flickr.com/photos/tags/thatch/",
            ["This URL shows photos tagged with", "thatch"],
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
        assert text in resp.text.replace("&nbsp;", " ").replace("&#39;", "'")


def test_cant_find_resource_is_error(client: FlaskClient, api: FlickrApi) -> None:
    resp = client.get(
        "/see_photos?flickr_url=https://www.flickr.com/photos/doesnotexist/12345678901234567890"
    )

    assert resp.status_code == 200
    assert "Unable to find" in resp.text


def test_it_doesnt_show_date_taken_if_not_known(
    client: FlaskClient, api: FlickrApi
) -> None:
    resp = client.get(
        "/see_photos?flickr_url=https://www.flickr.com/photos/sdasmarchives/50567413447"
    )

    assert resp.status_code == 200
    assert "taken None" not in resp.text


def test_empty_url_redirects_to_homepage(client: FlaskClient) -> None:
    resp = client.get("/see_photos?flickr_url=")

    assert resp.status_code == 302
    assert resp.headers["location"] == "/"
