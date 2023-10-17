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

import httpx
import hyperlink
from flickr_url_parser import parse_flickr_url

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
    elif categorised_url["type"] == "album":
        user_id = lookup_user_id_from_url(api, user_url=categorised_url["user_url"])

        user_info = get_user_info(api, user_id=user_id)

        photoset_resp = api.call(
            "flickr.photosets.getInfo",
            user_id=user_id,
            photoset_id=categorised_url["album_id"],
        )
        photoset_title = photoset_resp.find(".//title").text

        return {
            "user_info": user_info,
            "photoset_title": photoset_title,
            **get_photos_in_photoset(
                api,
                user_id=user_id,
                photoset_id=categorised_url["album_id"],
                page=page,
            ),
        }
    elif categorised_url["type"] == "user":
        user_id = lookup_user_id_from_url(api, user_url=categorised_url["user_url"])

        return {
            "user_info": get_user_info(api, user_id=user_id),
            **get_public_photos_by_person(api, user_id=user_id, page=page),
        }
    elif categorised_url["type"] == "gallery":
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
    elif categorised_url["type"] == "tag":
        return get_photos_with_tag(api, tag=categorised_url["tag"], page=page)
    else:
        return {}
