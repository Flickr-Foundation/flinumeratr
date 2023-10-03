import datetime
import json

from flinumeratr.flickr_api import (
    get_licenses,
    get_photos_in_gallery,
    get_photos_in_group_pool,
    get_photos_in_photoset,
    get_public_photos_by_person,
    get_single_photo_info,
    lookup_license_code,
    lookup_group_nsid_from_url,
    lookup_user_nsid_from_url,
)

from fixtures import (
    GET_PHOTOS_IN_GALLERY,
    GET_PHOTOS_IN_PHOTOSET,
    GET_PUBLIC_PHOTOS_BY_PERSON,
    GET_PHOTOS_IN_GROUP_POOL,
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
        "10": {
            "name": "Public Domain Mark",
            "url": "https://creativecommons.org/publicdomain/mark/1.0/",
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
    }


def test_lookup_license_code(api):
    assert lookup_license_code(api, license_code="0") == {
        "name": "All Rights Reserved",
        "url": "",
    }


def test_get_single_photo_info(api):
    info = get_single_photo_info(api, photo_id="32812033543")

    assert info == {
        "title": "Puppy Kisses",
        "owner": "Coast Guard",
        "date_posted": datetime.datetime(2017, 3, 24, 17, 27, 52),
        "date_taken": datetime.datetime(2017, 2, 17, 0, 0),
        "sizes": [
            {
                "height": 75,
                "label": "Square",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c1b3784192_s.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/sq/",
                "width": 75,
            },
            {
                "height": 150,
                "label": "Large Square",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c1b3784192_q.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/q/",
                "width": 150,
            },
            {
                "height": 61,
                "label": "Thumbnail",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c1b3784192_t.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/t/",
                "width": 100,
            },
            {
                "height": 146,
                "label": "Small",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c1b3784192_m.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/s/",
                "width": 240,
            },
            {
                "height": 195,
                "label": "Small 320",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c1b3784192_n.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/n/",
                "width": 320,
            },
            {
                "height": 243,
                "label": "Small 400",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c1b3784192_w.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/w/",
                "width": 400,
            },
            {
                "height": 304,
                "label": "Medium",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c1b3784192.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/m/",
                "width": 500,
            },
            {
                "height": 389,
                "label": "Medium 640",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c1b3784192_z.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/z/",
                "width": 640,
            },
            {
                "height": 486,
                "label": "Medium 800",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c1b3784192_c.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/c/",
                "width": 800,
            },
            {
                "height": 623,
                "label": "Large",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c1b3784192_b.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/l/",
                "width": 1024,
            },
            {
                "height": 973,
                "label": "Large 1600",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_c34e251a30_h.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/h/",
                "width": 1600,
            },
            {
                "height": 1245,
                "label": "Large 2048",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_04e9bcc8a2_k.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/k/",
                "width": 2048,
            },
            {
                "height": 3145,
                "label": "Original",
                "media": "photo",
                "source": "https://live.staticflickr.com/2903/32812033543_41cc4e453a_o.jpg",
                "url": "https://www.flickr.com/photos/coast_guard/32812033543/sizes/o/",
                "width": 5172,
            },
        ],
        "license": {
            "name": "United States Government Work",
            "url": "http://www.usa.gov/copyright.shtml",
        },
        "url": "https://www.flickr.com/photos/coast_guard/32812033543/",
    }


def test_lookup_user_nsid_from_url(api):
    nsid = lookup_user_nsid_from_url(
        api, user_url="https://www.flickr.com/photos/britishlibrary/"
    )

    assert nsid == "12403504@N02"


def test_lookup_group_nsid_from_url(api):
    nsid = lookup_group_nsid_from_url(
        api, group_url="https://www.flickr.com/groups/slovenia/pool/"
    )

    assert nsid == "31849566@N00"


def test_get_photos_in_photoset(api):
    resp = get_photos_in_photoset(
        api,
        user_nsid="12403504@N02",
        photoset_id="72157638792012173",
        page=1,
        per_page=3,
    )

    assert resp == GET_PHOTOS_IN_PHOTOSET


def test_get_photos_in_photoset_can_paginate(api):
    all_resp = get_photos_in_photoset(
        api, user_nsid="12403504@N02", photoset_id="72157638792012173", page=1
    )

    # Getting the 5th page with a page size of 1 means getting the 5th image
    individual_resp = get_photos_in_photoset(
        api,
        user_nsid="12403504@N02",
        photoset_id="72157638792012173",
        page=5,
        per_page=1,
    )

    assert individual_resp["photos"][0] == all_resp["photos"][4]


def test_get_public_photos_by_person(api):
    resp = get_public_photos_by_person(
        api,
        user_nsid="47265398@N04",
        page=1,
        per_page=5,
    )

    assert resp == GET_PUBLIC_PHOTOS_BY_PERSON


def test_get_public_photos_by_person_can_paginate(api):
    all_resp = get_public_photos_by_person(
        api,
        user_nsid="47265398@N04",
        page=1,
        per_page=5,
    )

    # Getting the 5th page with a page size of 1 means getting the 5th image
    individual_resp = get_public_photos_by_person(
        api,
        user_nsid="47265398@N04",
        page=5,
        per_page=1,
    )

    assert individual_resp["photos"][0] == all_resp["photos"][4]


def test_get_photos_in_group_pool(api):
    resp = get_photos_in_group_pool(api, group_nsid="31849566@N00", page=1, per_page=5)

    assert resp == GET_PHOTOS_IN_GROUP_POOL


def test_get_photos_in_gallery(api):
    resp = get_photos_in_gallery(
        api, gallery_id="72157722096057728", page=1, per_page=5
    )

    assert resp == GET_PHOTOS_IN_GALLERY
