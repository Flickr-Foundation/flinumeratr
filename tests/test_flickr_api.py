import datetime

import httpx

from flinumeratr.flickr_api import get_single_photo_info


def test_get_single_photo_info(api):
    info = get_single_photo_info(api, photo_id="32812033543")

    assert info == {
        "title": "Puppy Kisses",
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
        "url": "https://www.flickr.com/photos/coast_guard/32812033543/",
    }
