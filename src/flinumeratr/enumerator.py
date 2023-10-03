"""
This file contains the core logic for "flinumeration" -- that is,
taking any URL on Flickr.com, and identifying a list of photos
that are behind that URL.

The process of flinumeration is split into two steps:

    1.  Categorising the URL.  This means taking a URL, and working
        out what it points to, e.g. a single image, album, a user.

    2.  Getting results from the categorised URL.  This means taking
        the output of step 1, and calling the Flickr API to get the
        appropriate images.

"""

import hyperlink

from flinumeratr.flickr_api import get_single_photo_info


class NotAFlickrUrl(Exception):
    pass


class UnrecognisedUrl(Exception):
    pass


def categorise_flickr_url(url):
    """
    Categorises a Flickr URL, e.g. whether it's a single image, an album,
    a user.

    This is the first step of flinumeration.
    """
    u = hyperlink.URL.from_text(url.rstrip("/"))

    # If this URL doesn't come from Flickr.com, then we can't possibly classify
    # it as a Flickr URL!
    if u.host != "www.flickr.com":
        raise NotAFlickrUrl(url)

    # The URL for a single photo, e.g.
    # https://www.flickr.com/photos/coast_guard/32812033543/
    if len(u.path) == 3 and u.path[0] == "photos" and u.path[2].isnumeric():
        return {
            "type": "single_photo",
            "url": url,
            "photo_id": u.path[2],
        }

    if (
        len(u.path) == 5
        and u.path[0] == "photos"
        and u.path[2].isnumeric()
        and u.path[3] == "in"
        and u.path[4].startswith(("album-", "photolist-"))
    ):
        return {
            "type": "single_photo",
            "url": url,
            "photo_id": u.path[2],
        }

    # The URL for an album, e.g.
    # https://www.flickr.com/photos/cat_tac/albums/72157666833379009
    if (
        len(u.path) == 4
        and u.path[0] == "photos"
        and u.path[2] == "albums"
        and u.path[3].isnumeric()
    ):
        return {"type": "photoset", "url": url, "photoset_id": u.path[3]}

    raise UnrecognisedUrl(f"Unrecognised URL: {url}")


def get_photo_data(api, *, categorised_url):
    """
    Given some data about a categorised URL, actually fetch a list of photos
    from Flickr.

    This is the second step of flinumeration.
    """
    if categorised_url["type"] == "single_photo":
        return [get_single_photo_info(api, photo_id=categorised_url["photo_id"])]
    else:
        return []


def flinumerate(api, *, url):
    categorised_url = categorise_flickr_url(url)
    photos = get_photo_data(api, categorised_url=categorised_url)

    return {
        **categorised_url,
        "photos": photos,
    }
