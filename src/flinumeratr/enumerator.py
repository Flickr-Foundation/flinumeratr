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

from flinumeratr.flickr_api import (
    get_photos_in_group_pool,
    get_photos_in_photoset,
    get_public_photos_by_person,
    get_single_photo_info,
    lookup_group_nsid_from_url,
    lookup_user_nsid_from_url,
)


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
        return {
            "type": "photoset",
            "url": url,
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
            "photoset_id": u.path[3],
        }

    # The URL for a user, e.g.
    # https://www.flickr.com/photos/blueminds/
    # https://www.flickr.com/people/blueminds/
    # https://www.flickr.com/photos/blueminds/albums
    #
    if len(u.path) == 2 and u.path[0] in ("photos", "people"):
        return {
            "type": "people",
            "url": url,
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
        }

    if len(u.path) == 3 and u.path[0] == "photos" and u.path[2] == "albums":
        return {
            "type": "people",
            "url": url,
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
        }

    # URLs for a group, e.g.
    #
    #     https://www.flickr.com/groups/slovenia/pool
    #     https://www.flickr.com/groups/slovenia
    #
    if len(u.path) == 2 and u.path[0] == "groups":
        return {
            "type": "group",
            "url": url,
            "group_url": f"https://www.flickr.com/groups/{u.path[1]}",
        }

    if len(u.path) == 3 and u.path[0] == "groups" and u.path[2] == "pool":
        return {
            "type": "group",
            "url": url,
            "group_url": f"https://www.flickr.com/groups/{u.path[1]}",
        }

    raise UnrecognisedUrl(f"Unrecognised URL: {url}")


def get_photo_data(api, *, categorised_url, page):
    """
    Given some data about a categorised URL, actually fetch a list of photos
    from Flickr.

    This is the second step of flinumeration.
    """
    if categorised_url["type"] == "single_photo":
        return {
            "photos": [get_single_photo_info(api, photo_id=categorised_url["photo_id"])]
        }
    elif categorised_url["type"] == "photoset":
        user_nsid = lookup_user_nsid_from_url(api, user_url=categorised_url["user_url"])

        return get_photos_in_photoset(
            api,
            user_nsid=user_nsid,
            photoset_id=categorised_url["photoset_id"],
            page=page,
        )
    elif categorised_url["type"] == "people":
        user_nsid = lookup_user_nsid_from_url(api, user_url=categorised_url["user_url"])

        return get_public_photos_by_person(api, user_nsid=user_nsid, page=page)
    elif categorised_url["type"] == "group":
        group_nsid = lookup_group_nsid_from_url(
            api, group_url=categorised_url["group_url"]
        )

        return get_photos_in_group_pool(api, group_nsid=group_nsid, page=page)
    else:
        return {}


def flinumerate(api, *, url, page):
    categorised_url = categorise_flickr_url(url)
    photos = get_photo_data(api, categorised_url=categorised_url, page=page)

    return {
        **categorised_url,
        **photos,
    }
