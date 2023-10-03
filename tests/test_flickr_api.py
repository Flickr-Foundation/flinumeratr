import datetime

from flinumeratr.flickr_api import (
    get_licenses,
    get_photos_in_photoset,
    get_single_photo_info,
    lookup_license_code,
    lookup_user_id_from_url,
)


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


def test_lookup_user_id_from_url(api):
    nsid = lookup_user_id_from_url(
        api, user_url="https://www.flickr.com/photos/britishlibrary/"
    )

    assert nsid == "12403504@N02"


def test_get_photos_in_photoset(api):
    resp = get_photos_in_photoset(
        api,
        user_nsid="12403504@N02",
        photoset_id="72157638792012173",
        page=1,
        per_page=3,
    )

    assert resp == {
        "page_count": 34,
        "photos": [
            {
                "date_posted": datetime.datetime(2013, 12, 5, 18, 55, 30),
                "date_taken": datetime.datetime(2013, 12, 5, 18, 55, 30),
                "license": {
                    "name": "No known copyright restrictions",
                    "url": "https://www.flickr.com/commons/usage/",
                },
                "owner": "The British Library",
                "sizes": [
                    {
                        "height": 75,
                        "label": "Square",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/3755/11225186786_d0316726e1_s.jpg",
                        "width": 75,
                    },
                    {
                        "height": 100,
                        "label": "Thumbnail",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/3755/11225186786_d0316726e1_t.jpg",
                        "width": 77,
                    },
                    {
                        "height": 240,
                        "label": "Small",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/3755/11225186786_d0316726e1_m.jpg",
                        "width": 186,
                    },
                    {
                        "height": 500,
                        "label": "Medium",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/3755/11225186786_d0316726e1.jpg",
                        "width": 387,
                    },
                    {
                        "height": 1777,
                        "label": "Original",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/3755/11225186786_141efb0b4d_o.jpg",
                        "width": 1377,
                    },
                ],
                "title": 'British Library digitised image from page 99 of "The '
                "Cathedral Churches of Ireland: being notes, more "
                "especially on the smaller and less known of those "
                'churches, etc"',
                "url": "https://www.flickr.com/photos/britishlibrary/11225186786",
            },
            {
                "date_posted": datetime.datetime(2013, 11, 24, 13, 39, 48),
                "date_taken": datetime.datetime(2013, 11, 24, 13, 39, 48),
                "license": {
                    "name": "No known copyright restrictions",
                    "url": "https://www.flickr.com/commons/usage/",
                },
                "owner": "The British Library",
                "sizes": [
                    {
                        "height": 75,
                        "label": "Square",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/2874/11027979564_c8cf42af86_s.jpg",
                        "width": 75,
                    },
                    {
                        "height": 61,
                        "label": "Thumbnail",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/2874/11027979564_c8cf42af86_t.jpg",
                        "width": 100,
                    },
                    {
                        "height": 146,
                        "label": "Small",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/2874/11027979564_c8cf42af86_m.jpg",
                        "width": 240,
                    },
                    {
                        "height": 303,
                        "label": "Medium",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/2874/11027979564_c8cf42af86.jpg",
                        "width": 500,
                    },
                    {
                        "height": 2451,
                        "label": "Original",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/2874/11027979564_dde17ab292_o.jpg",
                        "width": 1487,
                    },
                ],
                "title": 'British Library digitised image from page 36 of "A New '
                "and Popular Pictorial Description of England, Scotland, "
                "Ireland, Wales, and the British Islands. Embellished "
                "with several hundred handsome engravings ... Sixth "
                'thousand"',
                "url": "https://www.flickr.com/photos/britishlibrary/11027979564",
            },
            {
                "date_posted": datetime.datetime(2013, 12, 1, 7, 27, 24),
                "date_taken": datetime.datetime(2013, 12, 1, 7, 27, 24),
                "license": {
                    "name": "No known copyright restrictions",
                    "url": "https://www.flickr.com/commons/usage/",
                },
                "owner": "The British Library",
                "sizes": [
                    {
                        "height": 75,
                        "label": "Square",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/3693/11146804456_f9cecc2443_s.jpg",
                        "width": 75,
                    },
                    {
                        "height": 57,
                        "label": "Thumbnail",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/3693/11146804456_f9cecc2443_t.jpg",
                        "width": 100,
                    },
                    {
                        "height": 136,
                        "label": "Small",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/3693/11146804456_f9cecc2443_m.jpg",
                        "width": 240,
                    },
                    {
                        "height": 283,
                        "label": "Medium",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/3693/11146804456_f9cecc2443.jpg",
                        "width": 500,
                    },
                    {
                        "height": 2368,
                        "label": "Original",
                        "media": "photo",
                        "source": "https://live.staticflickr.com/3693/11146804456_4ba65fbed5_o.jpg",
                        "width": 1342,
                    },
                ],
                "title": "British Library digitised image from page 163 of "
                '"History of the Hospital and School in Glasgow founded '
                "by George and Thomas Hutcheson, of Lambhill, A.D. "
                '1639-41, with notices of the founders, etc"',
                "url": "https://www.flickr.com/photos/britishlibrary/11146804456",
            },
        ],
    }


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
