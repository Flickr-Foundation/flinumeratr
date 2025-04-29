from flickr_api import FlickrApi

from flinumeratr.flickr_api import get_photos_in_user_photostream


def test_empty_result_if_no_public_photos(api: FlickrApi) -> None:
    """
    If a user doesn't have any public photos, we get an empty
    result back.
    """
    # This is a user who doesn't have any public photos.
    #
    # I found them by looking for users on the Flickr help forums who wanted
    # to make all their photos private:
    # https://www.flickr.com/help/forum/en-us/72157668446667394/
    photos = get_photos_in_user_photostream(api, user_id="51635425@N00")

    assert photos == {"count_pages": 1, "count_photos": 0, "photos": []}
