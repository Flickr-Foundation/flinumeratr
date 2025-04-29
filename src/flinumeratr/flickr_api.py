from xml.etree import ElementTree as ET

from flickr_api import FlickrApi, ResourceNotFound
from flickr_api.models import Size, User
from flickr_api.parsers import create_user, parse_date_taken, parse_timestamp
from flickr_url_parser import ParseResult
from nitrate.xml import find_required_elem, find_required_text

from .models import (
    CollectionOfPhotos,
    GroupInfo,
    PhotosInAlbum,
    PhotosInGallery,
    PhotosInGroup,
    Photo,
    PhotosFromUrl,
)


def get_photos_from_flickr_url(
    api: FlickrApi, parsed_url: ParseResult
) -> PhotosFromUrl:
    """
    Given a URL on Flickr.com that's been parsed with flickr-url-parser,
    return the photos at that URL (if possible).
    """
    if parsed_url["type"] == "single_photo":
        photo = api.get_single_photo(photo_id=parsed_url["photo_id"])

        return {
            "url": photo["url"],
            "image_url": get_image_url(photo["sizes"], desired_size="Medium"),
            "title": photo["title"],
            "owner_url": photo["owner"]["profile_url"],
            "owner_name": photo["owner"]["realname"] or photo["owner"]["username"],
            "date_taken": photo["date_taken"],
            "date_posted": photo["date_posted"],
            "license": photo["license"],
        }
    elif parsed_url["type"] == "album":
        return get_photos_in_album(
            api,
            user_url=parsed_url["user_url"],
            album_id=parsed_url["album_id"],
            page=parsed_url["page"],
            per_page=100,
        )
    elif parsed_url["type"] == "user":
        return get_photos_in_user_photostream(
            api, user_url=parsed_url["user_url"], page=parsed_url["page"], per_page=100
        )
    elif parsed_url["type"] == "gallery":
        return get_photos_in_gallery(
            api,
            gallery_id=parsed_url["gallery_id"],
            page=parsed_url["page"],
            per_page=100,
        )
    elif parsed_url["type"] == "group":
        return get_photos_in_group_pool(
            api,
            group_url=parsed_url["group_url"],
            page=parsed_url["page"],
            per_page=100,
        )
    elif parsed_url["type"] == "tag":
        return get_photos_with_tag(
            api, tag=parsed_url["tag"], page=parsed_url["page"], per_page=100
        )
    else:  # pragma: no cover
        raise TypeError(f"Unrecognised URL type: {parsed_url['type']}")


def _from_collection_photo(
    api: FlickrApi, photo_elem: ET.Element, owner: User | None
) -> Photo:
    """
    Given a <photo> element from a collection response, extract all the photo info.
    """
    photo_id = photo_elem.attrib["id"]

    if owner is None:
        owner = create_user(
            user_id=photo_elem.attrib["owner"],
            username=photo_elem.attrib["ownername"],
            realname=photo_elem.attrib.get("realname"),
            path_alias=photo_elem.attrib["pathalias"],
        )

    assert owner is not None

    license = api.lookup_license_by_id(id=photo_elem.attrib["license"])

    title = photo_elem.attrib["title"] or None

    date_posted = parse_timestamp(photo_elem.attrib["dateupload"])
    date_taken = parse_date_taken(
        value=photo_elem.attrib["datetaken"],
        granularity=photo_elem.attrib["datetakengranularity"],
        unknown=photo_elem.attrib["datetakenunknown"] == "1",
    )

    assert owner["photos_url"].endswith("/")
    url = owner["photos_url"] + photo_id + "/"

    sizes = parse_sizes(photo_elem)

    return {
        "url": url,
        "image_url": get_image_url(sizes, desired_size="Medium"),
        "title": title,
        "owner_url": owner["profile_url"],
        "owner_name": owner["realname"] or owner["username"],
        "date_taken": date_taken,
        "date_posted": date_posted,
        "license": license,
    }


def parse_sizes(photo_elem: ET.Element) -> list[Size]:
    """
    Get a list of sizes from a photo in a collection response.
    """
    # When you get a collection of photos (e.g. in an album)
    # you can get some of the sizes on the <photo> element, e.g.
    #
    #     <
    #       photo
    #       url_t="https://live.staticflickr.com/2893/1234567890_t.jpg"
    #       height_t="78"
    #       width_t="100"
    #       …
    #     />
    #
    sizes: list[Size] = []

    for suffix, label in [
        ("sq", "Square"),
        ("q", "Large Square"),
        ("t", "Thumbnail"),
        ("s", "Small"),
        ("m", "Medium"),
        ("l", "Large"),
        ("o", "Original"),
    ]:
        try:
            media = photo_elem.attrib["media"]

            if media not in ("video", "photo"):  # pragma: no cover
                raise ValueError(f"Unrecognised media: {media!r}")

            sizes.append(
                {
                    "height": int(photo_elem.attrib[f"height_{suffix}"]),
                    "width": int(photo_elem.attrib[f"width_{suffix}"]),
                    "label": label,
                    "media": media,  # type: ignore
                    "source": photo_elem.attrib[f"url_{suffix}"],
                }
            )
        except KeyError:
            pass

    return sizes


extras = [
    "license",
    "date_upload",
    "date_taken",
    "owner_name",
    "url_sq",
    "url_t",
    "url_s",
    "url_m",
    "url_o",
    "media",
    "realname",
    "path_alias",
]


def _create_collection(
    api: FlickrApi, collection_elem: ET.Element, owner: User | None = None
) -> CollectionOfPhotos:
    """
    This gets pagination information and extracts individual <photo>
    elements from a collection response.
    """
    photos = [
        _from_collection_photo(api, photo_elem, owner=owner)
        for photo_elem in collection_elem.findall("photo")
    ]

    # The wrapper element includes a couple of attributes related
    # to pagination, e.g.
    #
    #     <photoset pages="1" total="2" …>
    #
    count_pages = int(collection_elem.attrib["pages"])
    count_photos = int(collection_elem.attrib["total"])

    return {
        "photos": photos,
        "count_pages": count_pages,
        "count_photos": count_photos,
    }


def get_photos_in_album(
    api: FlickrApi,
    album_id: str,
    user_id: str | None = None,
    user_url: str | None = None,
    page: int = 1,
    per_page: int = 10,
) -> PhotosInAlbum:
    """
    Get a page of photos from an album.

    You need to pass a numeric album ID and one of the ``user_id`` or ``user_url``.

    For example, if the album URL is

        https://www.flickr.com/photos/158685238@N03/albums/72177720313849533/

    then you need to pass one of:

        {"album_id": "72177720313849533", "user_id": "158685238@N03"}
        {"album_id": "72177720313849533", "user_url": "https://www.flickr.com/photos/158685238@N03/"}

    """
    user_id = api._ensure_user_id(user_id=user_id, user_url=user_url)

    return _get_photos_in_album(
        api, user_id=user_id, album_id=album_id, page=page, per_page=per_page
    )


def _get_photos_in_album(
    api: FlickrApi, *, user_id: str, album_id: str, page: int, per_page: int
) -> PhotosInAlbum:
    """
    Get a page of photos from an album.
    """
    # https://www.flickr.com/services/api/flickr.photosets.getPhotos.html
    resp = api.call(
        method="flickr.photosets.getPhotos",
        params={
            "user_id": user_id,
            "photoset_id": album_id,
            "extras": ",".join(extras),
            "page": page,
            "per_page": per_page,
        },
        exceptions={
            "1": ResourceNotFound(f"Could not find album with ID: {album_id!r}"),
            "2": ResourceNotFound(f"Could not find user with ID: {user_id!r}"),
        },
    )

    # Albums are always non-empty, so we know we'll find something here
    photoset_elem = find_required_elem(resp, path="photoset")
    photo_elem = find_required_elem(photoset_elem, path="photo")

    owner = create_user(
        user_id=photoset_elem.attrib["owner"],
        username=photoset_elem.attrib["ownername"],
        realname=photo_elem.attrib.get("realname"),
        path_alias=photo_elem.attrib["pathalias"],
    )

    album_title = photoset_elem.attrib["title"]

    return {
        **_create_collection(api, photoset_elem, owner=owner),
        "album": {
            "owner": owner,
            "title": album_title,
        },
    }


def get_photos_in_gallery(
    api: FlickrApi, *, gallery_id: str, page: int = 1, per_page: int = 10
) -> PhotosInGallery:
    """
    Get a page of photos in a gallery.
    """
    # https://www.flickr.com/services/api/flickr.galleries.getPhotos.html
    resp = api.call(
        method="flickr.galleries.getPhotos",
        params={
            "gallery_id": gallery_id,
            "get_gallery_info": "1",
            "extras": ",".join(extras),
            "page": page,
            "per_page": per_page,
        },
        exceptions={
            "1": ResourceNotFound(f"Could not find gallery with ID: {gallery_id!r}")
        },
    )

    gallery_elem = find_required_elem(resp, path="gallery")

    gallery_title = find_required_text(gallery_elem, path="title")
    gallery_owner_name = gallery_elem.attrib["username"]

    photos_elem = find_required_elem(resp, path="photos")

    return {
        **_create_collection(api, photos_elem),
        "gallery": {"owner_name": gallery_owner_name, "title": gallery_title},
    }


def get_photos_in_user_photostream(
    api: FlickrApi,
    user_id: str | None = None,
    user_url: str | None = None,
    page: int = 1,
    per_page: int = 10,
) -> CollectionOfPhotos:
    """
    Get a page of photos from a user's photostream.

    You need to pass either the ``user_id`` or ``user_url``.

    For example, if the person's URL is

        https://www.flickr.com/photos/158685238@N03/

    then you need to pass one of:

        {"user_id": "158685238@N03"}
        {"user_url": "https://www.flickr.com/photos/158685238@N03/"}

    """
    user_id = api._ensure_user_id(user_id=user_id, user_url=user_url)

    # See https://www.flickr.com/services/api/flickr.people.getPublicPhotos.html
    resp = api.call(
        method="flickr.people.getPublicPhotos",
        params={
            "user_id": user_id,
            "extras": ",".join(extras),
            "page": page,
            "per_page": per_page,
        },
        exceptions={"1": ResourceNotFound(f"Could not find user with ID: {user_id!r}")},
    )

    first_photo = resp.find(".//photo")

    # The user hasn't uploaded any photos
    if first_photo is None:
        return {"count_pages": 1, "count_photos": 0, "photos": []}

    owner = create_user(
        user_id=first_photo.attrib["owner"],
        username=first_photo.attrib["ownername"],
        realname=first_photo.attrib.get("realname"),
        path_alias=first_photo.attrib["pathalias"],
    )

    photos_elem = find_required_elem(resp, path="photos")

    return _create_collection(api, photos_elem, owner=owner)


def _lookup_group_from_url(api: FlickrApi, *, url: str) -> GroupInfo:
    """
    Given the link to a group's photos or profile, return some info.
    """
    # See https://www.flickr.com/services/api/flickr.urls.lookupGroup.html
    resp = api.call(
        method="flickr.urls.lookupGroup",
        params={"url": url},
        exceptions={"1": ResourceNotFound(f"Could not find group with URL: {url!r}")},
    )

    # The lookupUser response is of the form:
    #
    #       <group id="34427469792@N01">
    #         <groupname>FlickrCentral</groupname>
    #       </group>
    #
    group_elem = find_required_elem(resp, path=".//group")

    return {
        "id": group_elem.attrib["id"],
        "name": find_required_text(group_elem, path="groupname"),
    }


def get_photos_in_group_pool(
    api: FlickrApi, *, group_url: str, page: int = 1, per_page: int = 10
) -> PhotosInGroup:
    """
    Get a page of photos in a group pool.
    """
    group_info = _lookup_group_from_url(api, url=group_url)

    # See https://www.flickr.com/services/api/flickr.groups.pools.getPhotos.html
    resp = api.call(
        method="flickr.groups.pools.getPhotos",
        params={
            "group_id": group_info["id"],
            "extras": ",".join(extras),
            "page": page,
            "per_page": per_page,
        },
    )

    photos_elem = find_required_elem(resp, path="photos")

    return {
        **_create_collection(api, photos_elem),
        "group": group_info,
    }


def get_photos_with_tag(
    api: FlickrApi, *, tag: str, page: int = 1, per_page: int = 10
) -> CollectionOfPhotos:
    """
    Get a page of photos in a tag.

    Note that tag pagination and ordering results can be inconsistent,
    especially for large tags -- it's tricky to do an "exhaustive" search
    of a Flickr tag.
    """
    resp = api.call(
        method="flickr.photos.search",
        params={
            "tags": tag,
            "page": page,
            "per_page": per_page,
            # This is so we get the same photos as you see on the "tag" page
            # under "All Photos Tagged XYZ" -- if you click the URL to the
            # full search results, you end up on a page like:
            #
            #     https://flickr.com/search/?sort=interestingness-desc&…
            #
            "sort": "interestingness-desc",
            "extras": ",".join(extras),
        },
    )

    photos_elem = find_required_elem(resp, path="photos")

    return _create_collection(api, photos_elem)


def get_image_url(sizes: list[Size], desired_size: str) -> str:
    """
    Given a list of sizes of Flickr photo, return the source of
    the desired size.
    """
    sizes_by_label = {s["label"]: s for s in sizes}

    # Flickr has a published list of possible sizes here:
    # https://www.flickr.com/services/api/misc.urls.html
    #
    # If the desired size isn't available, that means one of two things:
    #
    #   1.  The owner of this photo has done something to restrict downloads
    #       of their photo beyond a certain size.  But CC-licensed photos
    #       are always available to download, so that's not an issue for us.
    #   2.  This photo is smaller than the size we've asked for, in which
    #       case we fall back to the largest possible size.
    #
    try:
        return sizes_by_label[desired_size]["source"]
    except KeyError:  # pragma: no cover
        return max(sizes, key=lambda s: s["width"] or 0)["source"]
