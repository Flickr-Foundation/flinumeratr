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

import hyperlink


class NotAFlickrUrl(Exception):
    pass


class UnrecognisedUrl(Exception):
    pass


def categorise_flickr_url(url):
    """
    Categorises a Flickr URL, e.g. whether it's a single image, an album,
    a user.
    
    This is the first step of flinumeration.
    """
    u = hyperlink.URL.from_text(url.rstrip('/'))
    
    # If this URL doesn't come from Flickr.com, then we can't possibly classify
    # it as a Flickr URL!
    if u.host != 'www.flickr.com':
        raise NotAFlickrUrl(url)

    # The URL for a single photo, e.g.
    # https://www.flickr.com/photos/coast_guard/32812033543/
    if len(u.path) == 3 and u.path[0] == 'photos' and u.path[2].isnumeric():
        return {
            'type': 'single_photo',
            'url': url,
            'photo_id': u.path[2],
        }
    
    if len(u.path) == 5 and u.path[0] == 'photos' and u.path[2].isnumeric() and u.path[3] == 'in' and u.path[4].startswith(('album-', 'photolist-')):
        return {
            'type': 'single_photo',
            'url': url,
            'photo_id': u.path[2],
        }

    # The URL for an album, e.g.
    # https://www.flickr.com/photos/cat_tac/albums/72157666833379009
    if len(u.path) == 4 and u.path[0] == 'photos' and u.path[2] == 'albums' and u.path[3].isnumeric():
        return {
            'type': 'photoset',
            'url': url,
            'photoset_id': u.path[3]
        }

    raise UnrecognisedUrl(f"Unrecognised URL: {url}")
