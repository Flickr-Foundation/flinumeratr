import datetime

from flinumeratr.flickr_api import get_licenses, get_single_photo_info, lookup_user_id_from_url


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
    nsid = lookup_user_id_from_url(api, user_url="https://www.flickr.com/photos/britishlibrary/")
    
    assert nsid == "12403504@N02"
