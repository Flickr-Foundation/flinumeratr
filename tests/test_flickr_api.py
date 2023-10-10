import datetime
import json

import pytest

from flinumeratr.flickr_api import (
    get_licenses,
    get_photos_in_gallery,
    get_photos_in_group_pool,
    get_photos_in_photoset,
    get_photos_with_tag,
    get_public_photos_by_person,
    get_single_photo_info,
    get_user_info,
    lookup_license_code,
    lookup_group_id_from_url,
    lookup_user_id_from_url,
    ResourceNotFound,
)
from fixtures import (
    GET_PHOTOS_IN_GALLERY,
    GET_PHOTOS_IN_PHOTOSET,
    GET_PUBLIC_PHOTOS_BY_PERSON,
    GET_PHOTOS_IN_GROUP_POOL,
    GET_PHOTOS_WITH_TAG,
    GET_SINGLE_PHOTO,
)


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()


def test_get_licenses(api):
    assert get_licenses(api) == {
        "0": {"name": "All Rights Reserved", "url": ""},
        "1": {
            "name": "Attribution-NonCommercial-ShareAlike License",
            "url": "https://creativecommons.org/licenses/by-nc-sa/2.0/",
        },
        "2": {
            "name": "Attribution-NonCommercial License",
            "url": "https://creativecommons.org/licenses/by-nc/2.0/",
        },
        "3": {
            "name": "Attribution-NonCommercial-NoDerivs License",
            "url": "https://creativecommons.org/licenses/by-nc-nd/2.0/",
        },
        "4": {
            "name": "Attribution License",
            "url": "https://creativecommons.org/licenses/by/2.0/",
        },
        "5": {
            "name": "Attribution-ShareAlike License",
            "url": "https://creativecommons.org/licenses/by-sa/2.0/",
        },
        "6": {
            "name": "Attribution-NoDerivs License",
            "url": "https://creativecommons.org/licenses/by-nd/2.0/",
        },
        "7": {
            "name": "No known copyright restrictions",
            "url": "https://www.flickr.com/commons/usage/",
        },
        "8": {
            "name": "United States Government Work",
            "url": "http://www.usa.gov/copyright.shtml",
        },
        "9": {
            "name": "Public Domain Dedication (CC0)",
            "url": "https://creativecommons.org/publicdomain/zero/1.0/",
        },
        "10": {
            "name": "Public Domain Mark",
            "url": "https://creativecommons.org/publicdomain/mark/1.0/",
        },
    }


def test_lookup_license_code(api):
    assert lookup_license_code(api, license_code="0") == {
        "name": "All Rights Reserved",
        "url": "",
    }


def test_get_single_photo_info(api):
    info = get_single_photo_info(api, photo_id="32812033543")

    assert info == GET_SINGLE_PHOTO


@pytest.mark.parametrize(
    ["method", "params"],
    [
        (get_single_photo_info, {"photo_id": "123456789123456789"}),
        (
            lookup_user_id_from_url,
            {"user_url": "https://www.flickr.com/photos/doesnotexistnonono/"},
        ),
        (
            lookup_group_id_from_url,
            {"group_url": "https://www.flickr.com/groups/doesnotexist/pool/"},
        ),
        (
            get_photos_in_photoset,
            {"user_id": "12403504@N02", "photoset_id": "123456789123456789", "page": 1},
        ),
        (get_public_photos_by_person, {"user_id": "doesnotexist", "page": 1}),
        (get_photos_in_group_pool, {"group_id": "doesnotexist", "page": 1}),
        (get_photos_in_gallery, {"gallery_id": "doesnotexist", "page": 1}),
    ],
)
def test_methods_fail_if_not_found(api, method, params):
    with pytest.raises(ResourceNotFound):
        method(api, **params)


def test_lookup_user_id_from_url(api):
    id = lookup_user_id_from_url(
        api, user_url="https://www.flickr.com/photos/britishlibrary/"
    )

    assert id == "12403504@N02"


def test_lookup_group_id_from_url(api):
    id = lookup_group_id_from_url(
        api, group_url="https://www.flickr.com/groups/slovenia/pool/"
    )

    assert id == "31849566@N00"


def test_get_photos_in_photoset(api):
    resp = get_photos_in_photoset(
        api,
        user_id="12403504@N02",
        photoset_id="72157638792012173",
        page=1,
        per_page=3,
    )

    assert resp == GET_PHOTOS_IN_PHOTOSET


def test_get_photos_in_photoset_can_paginate(api):
    all_resp = get_photos_in_photoset(
        api, user_id="12403504@N02", photoset_id="72157638792012173", page=1
    )

    # Getting the 5th page with a page size of 1 means getting the 5th image
    individual_resp = get_photos_in_photoset(
        api,
        user_id="12403504@N02",
        photoset_id="72157638792012173",
        page=5,
        per_page=1,
    )

    assert individual_resp["photos"][0] == all_resp["photos"][4]


def test_get_public_photos_by_person(api):
    resp = get_public_photos_by_person(
        api,
        user_id="47265398@N04",
        page=1,
        per_page=5,
    )

    assert resp == GET_PUBLIC_PHOTOS_BY_PERSON


def test_get_public_photos_by_person_can_paginate(api):
    all_resp = get_public_photos_by_person(
        api,
        user_id="47265398@N04",
        page=1,
        per_page=5,
    )

    # Getting the 5th page with a page size of 1 means getting the 5th image
    individual_resp = get_public_photos_by_person(
        api,
        user_id="47265398@N04",
        page=5,
        per_page=1,
    )

    assert individual_resp["photos"][0] == all_resp["photos"][4]


def test_get_photos_in_group_pool(api):
    resp = get_photos_in_group_pool(api, group_id="31849566@N00", page=1, per_page=5)

    assert resp == GET_PHOTOS_IN_GROUP_POOL


def test_get_photos_in_gallery(api):
    resp = get_photos_in_gallery(
        api, gallery_id="72157722096057728", page=1, per_page=5
    )

    assert resp == GET_PHOTOS_IN_GALLERY


def test_get_photos_with_tag(api):
    resp = get_photos_with_tag(api, tag="tennis", page=1, per_page=5)

    assert resp == GET_PHOTOS_WITH_TAG


@pytest.mark.parametrize(
    ["user_id", "user_info"],
    [
        (
            "35591378@N03",
            {
                "realname": None,
                "user_id": "35591378@N03",
                "username": "Obama White House Archived",
            },
        ),
        (
            "47265398@N04",
            {
                "realname": "Alexander Lauterbach",
                "user_id": "47265398@N04",
                "username": "Alexander Lauterbach Photography",
            },
        ),
        
    ],
)
def test_get_user_info(api, user_id, user_info):
    assert get_user_info(api, user_id=user_id) == user_info
