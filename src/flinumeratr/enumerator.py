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

import sys
from typing import List, Union

# See https://mypy.readthedocs.io/en/stable/runtime_troubles.html#using-new-additions-to-the-typing-module
# See https://github.com/python/mypy/issues/8520
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from flickr_photos_api import (
    FlickrPhotosApi,
    SinglePhoto,
    PhotosInAlbum,
    CollectionOfPhotos,
    PhotosInGallery,
    PhotosInGroup,
)
from flickr_url_parser import ParseResult


class SinglePhotoData(TypedDict):
    photos: List[SinglePhoto]


PhotoData = Union[
    SinglePhotoData, PhotosInAlbum, CollectionOfPhotos, PhotosInGallery, PhotosInGroup
]


def get_photo_data(
    api: FlickrPhotosApi, *, parse_result: ParseResult, page: int
) -> PhotoData:
    """
    Given some data about a categorised URL, actually fetch a list of photos
    from Flickr.

    This is the second step of flinumeration.
    """
    if parse_result["type"] == "single_photo":
        photo = api.get_single_photo(photo_id=parse_result["photo_id"])

        return {"photos": [photo]}
    elif parse_result["type"] == "album":
        return api.get_photos_in_album(
            user_url=parse_result["user_url"],
            album_id=parse_result["album_id"],
            page=page,
        )
    elif parse_result["type"] == "user":
        return api.get_public_photos_by_user(
            user_url=parse_result["user_url"], page=page
        )
    elif parse_result["type"] == "gallery":
        return api.get_photos_in_gallery(
            gallery_id=parse_result["gallery_id"], page=page
        )
    elif parse_result["type"] == "group":
        return api.get_photos_in_group_pool(
            group_url=parse_result["group_url"], page=page
        )
    elif parse_result["type"] == "tag":
        return api.get_photos_with_tag(tag=parse_result["tag"], page=page)
    else:  # pragma: no cover
        raise ValueError(f"Unrecognised URL type: {parse_result['type']}")
