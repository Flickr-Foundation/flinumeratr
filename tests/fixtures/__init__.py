"""
This file contains some expected responses for the API tests.

These responses are large, so they're in a separate file to avoid
cluttering up the main test file.  They're stored as Python objects
to avoid any issues with serialisation (e.g. serialising `datetime`
values to JSON is annoying).
"""

import datetime


GET_PHOTOS_IN_PHOTOSET = {
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


GET_PUBLIC_PHOTOS_BY_PERSON = {
    "page_count": 73,
    "photos": [
        {
            "date_posted": datetime.datetime(2023, 9, 16, 15, 35, 25),
            "date_taken": datetime.datetime(2023, 9, 16, 17, 33, 41),
            "license": {"name": "All Rights Reserved", "url": ""},
            "owner": "Alexander Lauterbach Photography",
            "sizes": [
                {
                    "height": 75,
                    "label": "Square",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53191503745_17ab8888cf_s.jpg",
                    "width": 75,
                },
                {
                    "height": 67,
                    "label": "Thumbnail",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53191503745_17ab8888cf_t.jpg",
                    "width": 100,
                },
                {
                    "height": 160,
                    "label": "Small",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53191503745_17ab8888cf_m.jpg",
                    "width": 240,
                },
                {
                    "height": 333,
                    "label": "Medium",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53191503745_17ab8888cf.jpg",
                    "width": 500,
                },
            ],
            "title": "The Heart Nebula in Cassiopeia (IC 1805)",
            "url": "https://www.flickr.com/photos/blueminds/53191503745",
        },
        {
            "date_posted": datetime.datetime(2023, 8, 26, 15, 53, 2),
            "date_taken": datetime.datetime(2023, 6, 13, 8, 7, 52),
            "license": {"name": "All Rights Reserved", "url": ""},
            "owner": "Alexander Lauterbach Photography",
            "sizes": [
                {
                    "height": 75,
                    "label": "Square",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53142273497_5f1e1dc6b1_s.jpg",
                    "width": 75,
                },
                {
                    "height": 67,
                    "label": "Thumbnail",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53142273497_5f1e1dc6b1_t.jpg",
                    "width": 100,
                },
                {
                    "height": 160,
                    "label": "Small",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53142273497_5f1e1dc6b1_m.jpg",
                    "width": 240,
                },
                {
                    "height": 333,
                    "label": "Medium",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53142273497_5f1e1dc6b1.jpg",
                    "width": 500,
                },
            ],
            "title": "Jurassic Coast",
            "url": "https://www.flickr.com/photos/blueminds/53142273497",
        },
        {
            "date_posted": datetime.datetime(2023, 8, 5, 15, 33, 10),
            "date_taken": datetime.datetime(2023, 6, 8, 22, 3, 23),
            "license": {"name": "All Rights Reserved", "url": ""},
            "owner": "Alexander Lauterbach Photography",
            "sizes": [
                {
                    "height": 75,
                    "label": "Square",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53095231181_c8289ca518_s.jpg",
                    "width": 75,
                },
                {
                    "height": 67,
                    "label": "Thumbnail",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53095231181_c8289ca518_t.jpg",
                    "width": 100,
                },
                {
                    "height": 160,
                    "label": "Small",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53095231181_c8289ca518_m.jpg",
                    "width": 240,
                },
                {
                    "height": 333,
                    "label": "Medium",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53095231181_c8289ca518.jpg",
                    "width": 500,
                },
            ],
            "title": "Tajinastes",
            "url": "https://www.flickr.com/photos/blueminds/53095231181",
        },
        {
            "date_posted": datetime.datetime(2023, 7, 15, 13, 52, 17),
            "date_taken": datetime.datetime(2023, 6, 7, 21, 46, 23),
            "license": {"name": "All Rights Reserved", "url": ""},
            "owner": "Alexander Lauterbach Photography",
            "sizes": [
                {
                    "height": 75,
                    "label": "Square",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53046789782_681ab6ea0c_s.jpg",
                    "width": 75,
                },
                {
                    "height": 67,
                    "label": "Thumbnail",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53046789782_681ab6ea0c_t.jpg",
                    "width": 100,
                },
                {
                    "height": 160,
                    "label": "Small",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53046789782_681ab6ea0c_m.jpg",
                    "width": 240,
                },
                {
                    "height": 333,
                    "label": "Medium",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/53046789782_681ab6ea0c.jpg",
                    "width": 500,
                },
            ],
            "title": "Golden Sunset over Tenerife",
            "url": "https://www.flickr.com/photos/blueminds/53046789782",
        },
        {
            "date_posted": datetime.datetime(2023, 6, 24, 15, 20, 43),
            "date_taken": datetime.datetime(2023, 6, 22, 16, 1, 17),
            "license": {"name": "All Rights Reserved", "url": ""},
            "owner": "Alexander Lauterbach Photography",
            "sizes": [
                {
                    "height": 75,
                    "label": "Square",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/52998518188_579c979859_s.jpg",
                    "width": 75,
                },
                {
                    "height": 51,
                    "label": "Thumbnail",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/52998518188_579c979859_t.jpg",
                    "width": 100,
                },
                {
                    "height": 123,
                    "label": "Small",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/52998518188_579c979859_m.jpg",
                    "width": 240,
                },
                {
                    "height": 256,
                    "label": "Medium",
                    "media": "photo",
                    "source": "https://live.staticflickr.com/65535/52998518188_579c979859.jpg",
                    "width": 500,
                },
            ],
            "title": "the monster",
            "url": "https://www.flickr.com/photos/blueminds/52998518188",
        },
    ],
}
