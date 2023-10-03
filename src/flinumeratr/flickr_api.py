"""
This file contains some methods for calling the Flickr API.
"""

import datetime
import functools
import xml.etree.ElementTree as ET

import httpx


class FlickrApi:
    """
    This is a thin wrapper for calling the Flickr API.

    It doesn't do much interesting stuff; the goal is just to reduce boilerplate
    in the rest of the codebase, e.g. have the XML parsing in one place rather
    than repeated everywhere.
    """

    def __init__(self, *, api_key):
        self.client = httpx.Client(
            base_url="https://api.flickr.com/services/rest/",
            params={"api_key": api_key},
        )

    def call(self, method, /, **params):
        params["method"] = method

        resp = self.client.get(url="", params=params)
        resp.raise_for_status()

        # Note: the xml.etree.ElementTree is not secure against maliciously
        # constructed data (see warning in the Python docs [1]), but that's
        # fine here -- we're only using it for responses from the Flickr API,
        # which we trust.
        #
        # [1]: https://docs.python.org/3/library/xml.etree.elementtree.html
        return ET.fromstring(resp.text)


@functools.lru_cache
def get_licenses(api: FlickrApi):
    """
    Returns a list of licenses, arranged by code.
    """
    license_resp = api.call("flickr.photos.licenses.getInfo")

    result = {}

    for lic in license_resp.findall(".//license"):
        result[lic.attrib["id"]] = {
            "name": lic.attrib["name"],
            "url": lic.attrib["url"],
        }

    return result


@functools.lru_cache
def lookup_license_code(api: FlickrApi, *, license_code: str):
    """
    Given a license code from the Flickr API, return the license data.

    e.g. a Flickr API response might include a photo in the following form:

        <photo license="0" …>

    Then you'd call this function to find out what that means:

        >>> lookup_license_code(api, license_code="0")
        {"name": "All Rights Reserved", "url": ""}

    """
    licenses = get_licenses(api)
    return licenses[license_code]


def _parse_date_posted(p):
    # See https://www.flickr.com/services/api/misc.dates.html
    # e.g. '1490376472'
    return datetime.datetime.utcfromtimestamp(int(p))


def _parse_date_taken(p):
    # See https://www.flickr.com/services/api/misc.dates.html
    # e.g. '2017-02-17 00:00:00'
    #
    # TODO: Implement proper support for granularity in this function.
    return datetime.datetime.strptime(p, "%Y-%m-%d %H:%M:%S")


def get_single_photo_info(api: FlickrApi, *, photo_id: str):
    """
    Look up the information for a single photo.
    """
    info_resp = api.call("flickr.photos.getInfo", photo_id=photo_id)
    sizes_resp = api.call("flickr.photos.getSizes", photo_id=photo_id)

    # The getInfo response is a blob of XML of the form:
    #
    #       <?xml version="1.0" encoding="utf-8" ?>
    #       <rsp stat="ok">
    #       <photo license="8" …>
    #       	<owner
    #               nsid="30884892@N08
    #               username="U.S. Coast Guard"
    #               realname="Coast Guard" …
    #           >
    #       		…
    #       	</owner>
    #       	<title>Puppy Kisses</title>
    #       	<dates
    #               posted="1490376472"
    #               taken="2017-02-17 00:00:00"
    #               …
    #           />
    #       	<urls>
    #       		<url type="photopage">https://www.flickr.com/photos/coast_guard/32812033543/</url>
    #       	</urls>
    #           …
    #       </photo>
    #       </rsp>
    #
    title = info_resp.find(".//photo/title").text
    owner = info_resp.find(".//photo/owner").attrib["realname"]

    date_posted = _parse_date_posted(info_resp.find(".//photo/dates").attrib["posted"])

    date_taken = _parse_date_taken(info_resp.find(".//photo/dates").attrib["taken"])

    photo_page_url = info_resp.find('.//photo/urls/url[@type="photopage"]').text

    license = lookup_license_code(
        api, license_code=info_resp.find(".//photo").attrib["license"]
    )

    # The getSizes response is a blob of XML of the form:
    #
    #       <?xml version="1.0" encoding="utf-8" ?>
    #       <rsp stat="ok">
    #       <sizes canblog="0" canprint="0" candownload="1">
    #           <size
    #               label="Square"
    #               width="75"
    #               height="75"
    #               source="https://live.staticflickr.com/2903/32812033543_c1b3784192_s.jpg"
    #               url="https://www.flickr.com/photos/coast_guard/32812033543/sizes/sq/"
    #               media="photo"
    #           />
    #           <size
    #               label="Large Square"
    #               width="150"
    #               height="150"
    #               source="https://live.staticflickr.com/2903/32812033543_c1b3784192_q.jpg"
    #               url="https://www.flickr.com/photos/coast_guard/32812033543/sizes/q/"
    #               media="photo"
    #           />
    #           …
    #       </sizes>
    #       </rsp>
    #
    # Within this function, we just return all the sizes -- we leave it up to the
    # caller to decide which size is most appropriate for their purposes.
    sizes = [s.attrib for s in sizes_resp.findall(".//size")]

    for s in sizes:
        s["width"] = int(s["width"])
        s["height"] = int(s["height"])

    return {
        "title": title,
        "owner": owner,
        "date_posted": date_posted,
        "date_taken": date_taken,
        "license": license,
        "url": photo_page_url,
        "sizes": sizes,
    }


def lookup_user_nsid_from_url(api, *, user_url):
    """
    Given the link to a user's photos or profile, return their NSID.
    """
    resp = api.call("flickr.urls.lookupUser", url=user_url)

    # The lookupUser response is of the form:
    #
    #       <?xml version="1.0" encoding="utf-8" ?>
    #       <rsp stat="ok">
    #       <user id="12403504@N02">
    #       	<username>The British Library</username>
    #       </user>
    #       </rsp>
    #
    return resp.find(".//user").attrib["id"]


def lookup_group_nsid_from_url(api, *, group_url):
    """
    Given the link to a group's photos or profile, return their NSID.
    """
    resp = api.call("flickr.urls.lookupGroup", url=group_url)

    # The lookupUser response is of the form:
    #
    #       <group id="34427469792@N01">
    #         <groupname>FlickrCentral</groupname>
    #       </group>
    #
    return resp.find(".//group").attrib["id"]


def _call_get_photos_api(api, api_method, *, wrapper_element, **kwargs):
    """
    A wrapper for calling APIs that return lots of photos as an array of
    <photo> elements.
    """
    extras = [
        "license",
        "date_upload",
        "date_taken",
        "media",
        "owner_name",
        "path_alias",
        "url_sq",
        "url_t",
        "url_s",
        "url_m",
        "url_o",
    ]

    resp = api.call(
        api_method,
        **kwargs,
        extras=",".join(extras),
    )

    # The getPhotos response returns a list of IDs, of the form:
    #
    #       <photoset … pages="1">
    #           <photo
    #               …"
    #               title=""
    #               license="0"
    #               dateupload="1511798124"
    #               datetaken="2017-11-01 01:27:43"
    #               ownername="Cat_tac"
    #               url_sq="https://live.staticflickr.com/4529/38624477376_88d8b25499_s.jpg"
    #               height_sq="75"
    #               width_sq="75"
    #           />
    #           …
    #       </photoset>
    #
    page_count = int(resp.find(f".//{wrapper_element}").attrib["pages"])

    photos = []

    for p in resp.findall(".//photo"):
        # TODO: This is definitely a bit fragile and could do with refactoring/more
        # rigorous testing.  e.g.
        #
        #   -   Do we need all the fields here, or just some?  We could simplify the
        #       response both here and in `get_single_photo_info`.
        #
        sizes = []

        for suffix, label in [
            # TODO: Is this Square or Large Square?
            ("sq", "Square"),
            ("t", "Thumbnail"),
            ("s", "Small"),
            ("m", "Medium"),
            ("o", "Original"),
        ]:
            try:
                sizes.append(
                    {
                        "height": int(p.attrib[f"height_{suffix}"]),
                        "width": int(p.attrib[f"width_{suffix}"]),
                        "label": label,
                        "media": p.attrib["media"],
                        "source": p.attrib[f"url_{suffix}"],
                    }
                )
            except KeyError:
                pass

        photos.append(
            {
                "title": p.attrib["title"],
                "license": lookup_license_code(api, license_code=p.attrib["license"]),
                "owner": p.attrib["ownername"],
                "date_posted": _parse_date_posted(p.attrib["dateupload"]),
                "date_taken": _parse_date_taken(p.attrib["datetaken"]),
                "url": f"https://www.flickr.com/photos/{p.attrib['pathalias']}/{p.attrib['id']}",
                "sizes": sizes,
            }
        )

    return {"page_count": page_count, "photos": photos}


def get_photos_in_photoset(api, *, user_nsid, photoset_id, page, per_page=10):
    """
    Given a photoset (album) on Flickr, return a list of photos in the album.
    """
    return _call_get_photos_api(
        api,
        "flickr.photosets.getPhotos",
        # The response is wrapped in <photoset> … </photoset>
        wrapper_element="photoset",
        user_id=user_nsid,
        photoset_id=photoset_id,
        page=page,
        per_page=per_page,
    )


def get_public_photos_by_person(api, *, user_nsid, page, per_page=10):
    """
    Given a person (user) on Flickr, return a list of their public photos.
    """
    return _call_get_photos_api(
        api,
        "flickr.people.getPublicPhotos",
        # The response is wrapped in <photos> … </photos>
        wrapper_element="photos",
        user_id=user_nsid,
        page=page,
        per_page=per_page,
    )


def get_photos_in_group_pool(api, *, group_nsid, page, per_page=10):
    """
    Given a group on Flickr, return a list of photos in the group's pool.
    """
    return _call_get_photos_api(
        api,
        "flickr.groups.pools.getPhotos",
        # The response is wrapped in <photos> … </photos>
        wrapper_element="photos",
        group_id=group_nsid,
        page=page,
        per_page=per_page,
    )


def get_photos_in_gallery(api, *, gallery_id, page, per_page=10):
    """
    Given a group on Flickr, return a list of photos in the group's pool.
    """
    return _call_get_photos_api(
        api,
        "flickr.galleries.getPhotos",
        gallery_id=gallery_id,
        # The response is wrapped in <photos> … </photos>
        wrapper_element="photos",
        page=page,
        per_page=per_page,
    )
