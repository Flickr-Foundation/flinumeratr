import hyperlink


class NotAFlickrUrl(Exception):
    pass


class UnrecognisedUrl(Exception):
    pass


def categorise_flickr_url(url):
    """
    Categorises a Flickr URL, e.g. whether it's a single image, an album,
    a user.
    """
    u = hyperlink.URL.from_text(url)
    
    # If this URL doesn't come from Flickr.com, then we can't possibly classify
    # it as a Flickr URL!
    if u.host != 'www.flickr.com':
        raise NotAFlickrUrl(url)

    # The URL for a single photo, e.g.
    # https://www.flickr.com/photos/coast_guard/32812033543/
    if len(u.path) == 3 and u.path[0] == 'photos' and u.path[2].isnumeric():
        return {
            'type': 'single_image',
            'url': url,
            'photo_id': u.path[2],
        }
    
    if len(u.path) == 5 and u.path[0] == 'photos' and u.path[2].isnumeric() and u.path[3] == 'in' and u.path[4].startswith('photolist-'):
        return {
            'type': 'single_image',
            'url': url,
            'photo_id': u.path[2],
        }
    
    raise UnrecognisedUrl(f"Unrecognised URL: {url}")
