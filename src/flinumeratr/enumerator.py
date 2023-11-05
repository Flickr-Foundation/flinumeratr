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


def get_photo_data(api, *, parsed_url, page):
    """
    Given some data about a categorised URL, actually fetch a list of photos
    from Flickr.

    This is the second step of flinumeration.
    """
    if parsed_url["type"] == "single_photo":
        photo = api.get_single_photo(photo_id=parsed_url["photo_id"])

        return {"photos": [photo]}
    elif parsed_url["type"] == "album":
        return api.get_photos_in_album(
            user_url=parsed_url["user_url"], album_id=parsed_url["album_id"], page=page
        )
    elif parsed_url["type"] == "user":
        return api.get_public_photos_by_user(user_url=parsed_url["user_url"], page=page)
    elif parsed_url["type"] == "gallery":
        return api.get_photos_in_gallery(gallery_id=parsed_url["gallery_id"], page=page)
    elif parsed_url["type"] == "group":
        return api.get_photos_in_group_pool(
            group_url=parsed_url["group_url"], page=page
        )
    elif parsed_url["type"] == "tag":
        return api.get_photos_with_tag(tag=parsed_url["tag"], page=page)
    else:
        return {}
