import hyperlink


class UnrecognisedUrl(Exception):
    pass


def parse_flickr_url(url):
    raise UnrecognisedUrl(f"Unrecognised URL: {url}")
