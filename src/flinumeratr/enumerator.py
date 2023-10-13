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

import re

import hyperlink

from flinumeratr.base58 import is_base58, base58_decode
from flinumeratr.flickr_api import (
    get_photos_in_gallery,
    get_photos_in_group_pool,
    get_photos_in_photoset,
    get_photos_with_tag,
    get_public_photos_by_person,
    get_single_photo_info,
    get_user_info,
    lookup_group_id_from_url,
    lookup_user_id_from_url,
)


class NotAFlickrUrl(Exception):
    """
    Raised when somebody tries to flinumerate a URL which isn't from Flickr.
    """

    pass


class UnrecognisedUrl(Exception):
    """
    Raised when somebody tries to flinumerate a URL on Flickr, but we
    can't work out what photos are there.
    """

    pass


def is_page(path_component):
    return re.match(r"^page\d+$", path_component)


def categorise_flickr_url(url):
    """
    Categorises a Flickr URL, e.g. whether it's a single photo, an album,
    a user.

    This is the first step of flinumeration.
    """
    try:
        u = hyperlink.URL.from_text(url.rstrip("/"))

    # This is for anything which any string can't be parsed as a URL,
    # e.g. `https://https://`
    #
    # Arguably some of those might be malformed URLs from flickr.com,
    # but it's a rare enough edge case that this is fine.
    except hyperlink.URLParseError:
        raise NotAFlickrUrl(url)

    # Handle URLs without a scheme, e.g.
    #
    #     flickr.com/photos/1234
    #
    # We know what the user means, but the hyperlink URL parsing library
    # thinks this is just the path component, not a sans-HTTP URL.
    #
    # These lines convert this to a full HTTPS URL, i.e.
    #
    #     https://flickr.com/photos/1234
    #
    # which allows the rest of the logic in the function to do
    # the "right thing" with this URL.
    if not url.startswith("http") and u.path[0] in {
        "www.flickr.com",
        "flickr.com",
        "flic.kr",
    }:
        u = hyperlink.URL.from_text("https://" + url.rstrip("/"))

    # If this URL doesn't come from Flickr.com, then we can't possibly classify
    # it as a Flickr URL!
    is_long_url = u.host in {"www.flickr.com", "flickr.com"}
    is_short_url = u.host == "flic.kr"

    if not is_long_url and not is_short_url:
        raise NotAFlickrUrl(url)

    # The URL for a single photo, e.g.
    # https://www.flickr.com/photos/coast_guard/32812033543/
    if (
        is_long_url
        and len(u.path) == 3
        and u.path[0] == "photos"
        and u.path[2].isnumeric()
    ):
        return {
            "type": "single_photo",
            "photo_id": u.path[2],
        }

    if (
        is_long_url
        and len(u.path) == 5
        and u.path[0] == "photos"
        and u.path[2].isnumeric()
        and u.path[3] == "in"
        and u.path[4].startswith(("album-", "photolist-"))
    ):
        return {
            "type": "single_photo",
            "photo_id": u.path[2],
        }

    # The URL for a single photo, e.g.
    #
    #     https://flic.kr/p/2p4QbKN
    #
    # Here the photo ID is a base-58 conversion of the photo ID.
    # See https://www.flickr.com/groups/51035612836@N01/discuss/72157616713786392/
    if is_short_url and len(u.path) == 2 and u.path[0] == "p" and is_base58(u.path[1]):
        return {"type": "single_photo", "photo_id": base58_decode(u.path[1])}

    # The URL for an album, e.g.
    #
    #     https://www.flickr.com/photos/cat_tac/albums/72157666833379009
    #     https://www.flickr.com/photos/cat_tac/sets/72157666833379009
    #
    if (
        is_long_url
        and len(u.path) == 4
        and u.path[0] == "photos"
        and u.path[2] in {"albums", "sets"}
        and u.path[3].isnumeric()
    ):
        return {
            "type": "photoset",
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
            "photoset_id": u.path[3],
        }

    # The URL for a user, e.g.
    #
    #     https://www.flickr.com/photos/blueminds/
    #     https://www.flickr.com/people/blueminds/
    #     https://www.flickr.com/photos/blueminds/albums
    #     https://www.flickr.com/people/blueminds/page3
    #
    if is_long_url and len(u.path) == 2 and u.path[0] in ("photos", "people"):
        return {
            "type": "people",
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
        }

    if (
        is_long_url
        and len(u.path) == 3
        and u.path[0] == "photos"
        and u.path[2] == "albums"
    ):
        return {
            "type": "people",
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
        }

    if (
        is_long_url
        and len(u.path) == 3
        and u.path[0] == "photos"
        and is_page(u.path[2])
    ):
        return {
            "type": "people",
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
        }

    # URLs for a group, e.g.
    #
    #     https://www.flickr.com/groups/slovenia/pool
    #     https://www.flickr.com/groups/slovenia
    #     https://www.flickr.com/groups/slovenia/pool/page16
    #
    if is_long_url and len(u.path) == 2 and u.path[0] == "groups":
        return {
            "type": "group",
            "group_url": f"https://www.flickr.com/groups/{u.path[1]}",
        }

    if (
        is_long_url
        and len(u.path) == 3
        and u.path[0] == "groups"
        and u.path[2] == "pool"
    ):
        return {
            "type": "group",
            "group_url": f"https://www.flickr.com/groups/{u.path[1]}",
        }

    if (
        is_long_url
        and len(u.path) == 4
        and u.path[0] == "groups"
        and u.path[2] == "pool"
        and is_page(u.path[3])
    ):
        return {
            "type": "group",
            "group_url": f"https://www.flickr.com/groups/{u.path[1]}",
        }

    # URLs for a gallery, e.g.
    #
    #     https://www.flickr.com/photos/flickr/galleries/72157722096057728/
    #     https://www.flickr.com/photos/flickr/galleries/72157722096057728/page2
    #
    if (
        is_long_url
        and len(u.path) == 4
        and u.path[0] == "photos"
        and u.path[2] == "galleries"
        and u.path[3].isnumeric()
    ):
        return {"type": "galleries", "gallery_id": u.path[3]}

    if (
        is_long_url
        and len(u.path) == 5
        and u.path[0] == "photos"
        and u.path[2] == "galleries"
        and u.path[3].isnumeric()
        and is_page(u.path[4])
    ):
        return {"type": "galleries", "gallery_id": u.path[3]}

    # URL for a tag, e.g.
    #
    #     https://flickr.com/photos/tags/tennis/
    #     https://flickr.com/photos/tags/fluorspar/page1
    #
    if (
        is_long_url
        and len(u.path) == 3
        and u.path[0] == "photos"
        and u.path[1] == "tags"
    ):
        return {"type": "tags", "tag": u.path[2]}

    if (
        is_long_url
        and len(u.path) == 4
        and u.path[0] == "photos"
        and u.path[1] == "tags"
        and is_page(u.path[3])
    ):
        return {"type": "tags", "tag": u.path[2]}

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
        user_id = lookup_user_id_from_url(api, user_url=categorised_url["user_url"])

        user_info = get_user_info(api, user_id=user_id)

        photoset_resp = api.call(
            "flickr.photosets.getInfo",
            user_id=user_id,
            photoset_id=categorised_url["photoset_id"],
        )
        photoset_title = photoset_resp.find(".//title").text

        return {
            "user_info": user_info,
            "photoset_title": photoset_title,
            **get_photos_in_photoset(
                api,
                user_id=user_id,
                photoset_id=categorised_url["photoset_id"],
                page=page,
            ),
        }
    elif categorised_url["type"] == "people":
        user_id = lookup_user_id_from_url(api, user_url=categorised_url["user_url"])

        return {
            "user_info": get_user_info(api, user_id=user_id),
            **get_public_photos_by_person(api, user_id=user_id, page=page),
        }
    elif categorised_url["type"] == "galleries":
        gallery_resp = api.call(
            "flickr.galleries.getInfo", gallery_id=categorised_url["gallery_id"]
        )

        gallery_title = gallery_resp.find(".//title").text

        return {
            "gallery_title": gallery_title,
            **get_photos_in_gallery(
                api, gallery_id=categorised_url["gallery_id"], page=page
            ),
        }
    elif categorised_url["type"] == "group":
        group_id = lookup_group_id_from_url(api, group_url=categorised_url["group_url"])

        group_resp = api.call("flickr.groups.getInfo", group_id=group_id)
        group_name = group_resp.find(".//name").text

        return {
            "group_name": group_name,
            **get_photos_in_group_pool(api, group_id=group_id, page=page),
        }
    elif categorised_url["type"] == "tags":
        return get_photos_with_tag(api, tag=categorised_url["tag"], page=page)
    else:
        return {}
