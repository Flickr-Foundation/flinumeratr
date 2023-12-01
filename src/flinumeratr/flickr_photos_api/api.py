import functools
from typing import Dict, List, Optional, Union
import xml.etree.ElementTree as ET

from flickr_url_parser import ParseResult, parse_flickr_url
import httpx

from .exceptions import FlickrApiException, LicenseNotFound, ResourceNotFound
from .utils import (
    find_optional_text,
    find_required_elem,
    find_required_text,
    parse_date_posted,
    parse_date_taken,
    parse_date_taken_granularity,
    parse_safety_level,
    parse_sizes,
)
from ._types import (
    CollectionOfPhotos,
    DateTaken,
    GroupInfo,
    License,
    PhotosFromUrl,
    PhotosInAlbum,
    PhotosInGallery,
    PhotosInGroup,
    SinglePhoto,
    Size,
    User,
)


class BaseApi:
    """
    This is a thin wrapper for calling the Flickr API.

    It doesn't do much interesting stuff; the goal is just to reduce boilerplate
    in the rest of the codebase, e.g. have the XML parsing in one place rather
    than repeated everywhere.
    """

    def __init__(self, *, api_key: str, user_agent: str) -> None:
        self.client = httpx.Client(
            base_url="https://api.flickr.com/services/rest/",
            params={"api_key": api_key},
            headers={"User-Agent": user_agent},
        )

    def call(self, method: str, **params: Union[str, int]) -> ET.Element:
        resp = self.client.get(url="", params={"method": method, **params})
        resp.raise_for_status()

        # Note: the xml.etree.ElementTree is not secure against maliciously
        # constructed data (see warning in the Python docs [1]), but that's
        # fine here -- we're only using it for responses from the Flickr API,
        # which we trust.
        #
        # [1]: https://docs.python.org/3/library/xml.etree.elementtree.html
        xml = ET.fromstring(resp.text)

        # If the Flickr API call fails, it will return a block of XML like:
        #
        #       <rsp stat="fail">
        #       	<err
        #               code="1"
        #               msg="Photo &quot;1211111111111111&quot; not found (invalid ID)"
        #           />
        #       </rsp>
        #
        # Different API endpoints have different codes, and so we just throw
        # and let calling functions decide how to handle it.
        if xml.attrib["stat"] == "fail":
            errors = find_required_elem(xml, path=".//err").attrib

            # Although I haven't found any explicit documentation of this,
            # it seems like a pretty common convention that error code "1"
            # means "not found".
            if errors["code"] == "1":
                raise ResourceNotFound(method, **params)
            else:
                raise FlickrApiException(errors)

        return xml


class FlickrPhotosApi(BaseApi):
    @functools.lru_cache()
    def get_licenses(self) -> Dict[str, License]:
        """
        Returns a list of licenses, arranged by code.

        See https://www.flickr.com/services/api/flickr.photos.licenses.getInfo.htm
        """
        license_resp = self.call("flickr.photos.licenses.getInfo")

        result: Dict[str, License] = {}

        # Add a short ID which can be used to more easily refer to this
        # license throughout the codebase.
        license_ids = {
            "All Rights Reserved": "in-copyright",
            "Attribution-NonCommercial-ShareAlike License": "cc-by-nc-sa-2.0",
            "Attribution-NonCommercial License": "cc-by-nc-2.0",
            "Attribution-NonCommercial-NoDerivs License": "cc-by-nc-nd-2.0",
            "Attribution License": "cc-by-2.0",
            "Attribution-ShareAlike License": "cc-by-sa-2.0",
            "Attribution-NoDerivs License": "cc-by-nd-2.0",
            "No known copyright restrictions": "nkcr",
            "United States Government Work": "usgov",
            "Public Domain Dedication (CC0)": "cc0-1.0",
            "Public Domain Mark": "pdm",
        }

        license_labels = {
            "Attribution-NonCommercial-ShareAlike License": "CC BY-NC-SA 2.0",
            "Attribution-NonCommercial License": "CC BY-NC 2.0",
            "Attribution-NonCommercial-NoDerivs License": "CC BY-NC-ND 2.0",
            "Attribution License": "CC BY 2.0",
            "Attribution-ShareAlike License": "CC BY-SA 2.0",
            "Attribution-NoDerivs License": "CC BY-ND 2.0",
            "Public Domain Dedication (CC0)": "CC0 1.0",
        }

        for lic in license_resp.findall(".//license"):
            result[lic.attrib["id"]] = {
                "id": license_ids[lic.attrib["name"]],
                "label": license_labels.get(lic.attrib["name"], lic.attrib["name"]),
                "url": lic.attrib["url"] or None,
            }

        return result

    @functools.lru_cache(maxsize=None)
    def lookup_license_by_id(self, *, id: str) -> License:
        """
        Given a license ID from the Flickr API, return the license data.

        e.g. a Flickr API response might include a photo in the following form:

            <photo license="0" …>

        Then you'd call this function to find out what that means:

            >>> api.lookup_license_by_id(id="0")
            {"id": "in-copyright", "name": "All Rights Reserved", "url": None}

        See https://www.flickr.com/services/api/flickr.photos.licenses.getInfo.htm
        """
        licenses = self.get_licenses()

        try:
            return licenses[id]
        except KeyError:
            raise LicenseNotFound(license_id=id)

    def lookup_user_by_url(self, *, url: str) -> User:
        """
        Given the link to a user's photos or profile, return their info.

            >>> api.lookup_user_by_url(user_url="https://www.flickr.com/photos/britishlibrary/")
            {
                "id": "12403504@N02",
                "username": "The British Library",
                "realname": "British Library",
                "photos_url": "https://www.flickr.com/photos/britishlibrary/",
                "profile_url": "https://www.flickr.com/people/britishlibrary/",
            }

        See https://www.flickr.com/services/api/flickr.urls.lookupUser.htm
        See https://www.flickr.com/services/api/flickr.people.getInfo.htm

        """
        # The lookupUser response is of the form:
        #
        #       <user id="12403504@N02">
        #       	<username>The British Library</username>
        #       </user>
        #
        lookup_resp = self.call("flickr.urls.lookupUser", url=url)
        user_id = find_required_elem(lookup_resp, path=".//user").attrib["id"]

        # The getInfo response is of the form:

        #     <person id="12403504@N02"…">
        #   	<username>The British Library</username>
        #       <realname>British Library</realname>
        #       <photosurl>https://www.flickr.com/photos/britishlibrary/</photosurl>
        #       <profileurl>https://www.flickr.com/people/britishlibrary/</profileurl>
        #       …
        #     </person>
        #
        info_resp = self.call("flickr.people.getInfo", user_id=user_id)
        username = find_required_text(info_resp, path=".//username")
        photos_url = find_required_text(info_resp, path=".//photosurl")
        profile_url = find_required_text(info_resp, path=".//profileurl")

        # If the user hasn't set a realname in their profile, the element
        # will be absent from the response.
        realname_elem = info_resp.find(path=".//realname")

        if realname_elem is None:
            realname = None
        else:
            realname = realname_elem.text

        return {
            "id": user_id,
            "username": username,
            "realname": realname,
            "photos_url": photos_url,
            "profile_url": profile_url,
        }

    def _get_date_taken(
        self, *, value: str, granularity: str, unknown: bool
    ) -> DateTaken:
        # Note: we intentionally omit sending any 'date taken' information
        # to callers if it's unknown.
        #
        # There will be a value in the API response, but if the taken date
        # is unknown, it's defaulted to the date the photo was posted.
        # See https://www.flickr.com/services/api/misc.dates.html
        #
        # This value isn't helpful to callers, so we omit it.  This reduces
        # the risk of somebody skipping the ``unknown`` parameter and using
        # the value in the wrong place.
        if unknown:
            return {"unknown": True}
        else:
            return {
                "value": parse_date_taken(value),
                "granularity": parse_date_taken_granularity(granularity),
                "unknown": False,
            }

    def get_single_photo(self, *, photo_id: str) -> SinglePhoto:
        """
        Look up the information for a single photo.
        """
        info_resp = self.call("flickr.photos.getInfo", photo_id=photo_id)
        sizes_resp = self.call("flickr.photos.getSizes", photo_id=photo_id)

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
        #           <description>Seaman Nina Bowen shows …</description>
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
        photo_elem = find_required_elem(info_resp, path=".//photo")

        title = find_optional_text(photo_elem, path="title")
        description = find_optional_text(photo_elem, path="description")

        owner_elem = find_required_elem(photo_elem, path="owner")
        user_id = owner_elem.attrib["nsid"]
        path_alias = owner_elem.attrib["path_alias"] or user_id

        owner: User = {
            "id": user_id,
            "username": owner_elem.attrib["username"],
            "realname": owner_elem.attrib["realname"] or None,
            "photos_url": f"https://www.flickr.com/photos/{path_alias}/",
            "profile_url": f"https://www.flickr.com/people/{path_alias}/",
        }

        dates = find_required_elem(photo_elem, path="dates").attrib

        date_posted = parse_date_posted(dates["posted"])

        date_taken = self._get_date_taken(
            value=dates["taken"],
            granularity=dates["takengranularity"],
            unknown=dates["takenunknown"] == "1",
        )

        photo_page_url = find_required_text(
            photo_elem, path='.//urls/url[@type="photopage"]'
        )

        license = self.lookup_license_by_id(id=photo_elem.attrib["license"])

        safety_level = parse_safety_level(photo_elem.attrib["safety_level"])

        # The originalformat parameter will only be returned if the user
        # allows downloads of the photo.
        #
        # We only need this parameter for photos that can be uploaded to
        # Wikimedia Commons.  All CC-licensed photos allow downloads, so
        # we'll always get this parameter for those photos.
        #
        # See https://www.flickr.com/help/forum/32218/
        # See https://www.flickrhelp.com/hc/en-us/articles/4404079715220-Download-permissions
        original_format = photo_elem.get("originalformat")

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
        sizes: List[Size] = []

        for s in sizes_resp.findall(".//size"):
            sizes.append(
                {
                    "label": s.attrib["label"],
                    "width": int(s.attrib["width"]),
                    "height": int(s.attrib["height"]),
                    "media": s.attrib["media"],
                    "source": s.attrib["source"],
                }
            )

        return {
            "id": photo_id,
            "title": title,
            "description": description,
            "owner": owner,
            "date_posted": date_posted,
            "date_taken": date_taken,
            "safety_level": safety_level,
            "license": license,
            "url": photo_page_url,
            "sizes": sizes,
            "original_format": original_format,
        }

    # There are a bunch of similar flickr.XXX.getPhotos methods;
    # these are some constants and utility methods to help when
    # calling them.
    extras = [
        "license",
        "date_upload",
        "date_taken",
        "media",
        "original_format",
        "owner_name",
        "url_sq",
        "url_t",
        "url_s",
        "url_m",
        "url_o",
        # These parameters aren't documented, but they're quite
        # useful for our purposes!
        "url_q",  # Large Square
        "url_l",  # Large
        "description",
        "safety_level",
        "realname",
    ]

    def _parse_collection_of_photos_response(
        self,
        elem: ET.Element,
        collection_owner: Optional[User] = None,
    ) -> CollectionOfPhotos:
        # The wrapper element includes a couple of attributes related
        # to pagination, e.g.
        #
        #     <photoset pages="1" total="2" …>
        #
        page_count = int(elem.attrib["pages"])
        total_photos = int(elem.attrib["total"])

        photos: List[SinglePhoto] = []

        for photo_elem in elem.findall(".//photo"):
            photo_id = photo_elem.attrib["id"]

            title = photo_elem.attrib["title"] or None
            description = find_optional_text(photo_elem, path="description")

            owner: User
            if collection_owner is None:
                path_alias = (
                    photo_elem.attrib.get("pathalias") or photo_elem.attrib["owner"]
                )

                owner = {
                    "id": photo_elem.attrib["owner"],
                    "username": photo_elem.attrib["ownername"],
                    "realname": photo_elem.attrib.get("realname") or None,
                    "photos_url": f"https://www.flickr.com/photos/{path_alias}/",
                    "profile_url": f"https://www.flickr.com/people/{path_alias}/",
                }
            else:
                owner = collection_owner

            assert owner["photos_url"].endswith("/")
            url = owner["photos_url"] + photo_id + "/"

            photos.append(
                {
                    "id": photo_id,
                    "title": title,
                    "description": description,
                    "date_posted": parse_date_posted(photo_elem.attrib["dateupload"]),
                    "date_taken": self._get_date_taken(
                        value=photo_elem.attrib["datetaken"],
                        granularity=photo_elem.attrib["datetakengranularity"],
                        unknown=photo_elem.attrib["datetakenunknown"] == "1",
                    ),
                    "license": self.lookup_license_by_id(
                        id=photo_elem.attrib["license"]
                    ),
                    "sizes": parse_sizes(photo_elem),
                    "original_format": photo_elem.attrib.get("originalformat"),
                    "safety_level": parse_safety_level(
                        photo_elem.attrib["safety_level"]
                    ),
                    "owner": owner,
                    "url": url,
                }
            )

        return {
            "page_count": page_count,
            "total_photos": total_photos,
            "photos": photos,
        }

    def get_photos_in_album(
        self, *, user_url: str, album_id: str, page: int = 1, per_page: int = 10
    ) -> PhotosInAlbum:
        """
        Get the photos in an album.
        """
        user = self.lookup_user_by_url(url=user_url)

        # https://www.flickr.com/services/api/flickr.photosets.getPhotos.html
        resp = self.call(
            "flickr.photosets.getPhotos",
            user_id=user["id"],
            photoset_id=album_id,
            extras=",".join(self.extras),
            page=page,
            per_page=per_page,
        )

        parsed_resp = self._parse_collection_of_photos_response(
            find_required_elem(resp, path=".//photoset"), collection_owner=user
        )

        # https://www.flickr.com/services/api/flickr.photosets.getInfo.html
        album_resp = self.call(
            "flickr.photosets.getInfo", user_id=user["id"], photoset_id=album_id
        )
        album_title = find_required_text(album_resp, path=".//title")

        return {
            "photos": parsed_resp["photos"],
            "page_count": parsed_resp["page_count"],
            "total_photos": parsed_resp["total_photos"],
            "album": {"owner": user, "title": album_title},
        }

    def get_photos_in_gallery(
        self, *, gallery_id: str, page: int = 1, per_page: int = 10
    ) -> PhotosInGallery:
        """
        Get the photos in a gallery.
        """
        # https://www.flickr.com/services/api/flickr.galleries.getPhotos.html
        resp = self.call(
            "flickr.galleries.getPhotos",
            gallery_id=gallery_id,
            get_gallery_info="1",
            extras=",".join(self.extras + ["path_alias"]),
            page=page,
            per_page=per_page,
        )

        parsed_resp = self._parse_collection_of_photos_response(
            find_required_elem(resp, path=".//photos")
        )

        gallery_elem = find_required_elem(resp, path=".//gallery")

        gallery_title = find_required_text(gallery_elem, path="title")
        gallery_owner_name = gallery_elem.attrib["username"]

        return {
            "photos": parsed_resp["photos"],
            "page_count": parsed_resp["page_count"],
            "total_photos": parsed_resp["total_photos"],
            "gallery": {"owner_name": gallery_owner_name, "title": gallery_title},
        }

    def get_public_photos_by_user(
        self, user_url: str, page: int = 1, per_page: int = 10
    ) -> CollectionOfPhotos:
        """
        Get all the public photos by a user on Flickr.
        """
        user = self.lookup_user_by_url(url=user_url)

        # See https://www.flickr.com/services/api/flickr.people.getPublicPhotos.html
        photos_resp = self.call(
            "flickr.people.getPublicPhotos",
            user_id=user["id"],
            extras=",".join(self.extras),
            page=page,
            per_page=per_page,
        )

        return self._parse_collection_of_photos_response(
            find_required_elem(photos_resp, path=".//photos"), collection_owner=user
        )

    def lookup_group_from_url(self, *, url: str) -> GroupInfo:
        """
        Given the link to a group's photos or profile, return some info.
        """
        resp = self.call("flickr.urls.lookupGroup", url=url)

        # The lookupUser response is of the form:
        #
        #       <group id="34427469792@N01">
        #         <groupname>FlickrCentral</groupname>
        #       </group>
        #
        group_elem = find_required_elem(resp, path=".//group")

        return {
            "id": group_elem.attrib["id"],
            "name": find_required_text(group_elem, path="groupname"),
        }

    def get_photos_in_group_pool(
        self, group_url: str, page: int = 1, per_page: int = 10
    ) -> PhotosInGroup:
        """
        Get all the photos in a group pool.
        """
        group_info = self.lookup_group_from_url(url=group_url)

        # See https://www.flickr.com/services/api/flickr.groups.pools.getPhotos.html
        photos_resp = self.call(
            "flickr.groups.pools.getPhotos",
            group_id=group_info["id"],
            extras=",".join(self.extras),
            page=page,
            per_page=per_page,
        )

        parsed_resp = self._parse_collection_of_photos_response(
            find_required_elem(photos_resp, path=".//photos")
        )

        return {
            "photos": parsed_resp["photos"],
            "page_count": parsed_resp["page_count"],
            "total_photos": parsed_resp["total_photos"],
            "group": group_info,
        }

    def get_photos_with_tag(
        self, tag: str, page: int = 1, per_page: int = 10
    ) -> CollectionOfPhotos:
        """
        Get all the photos that use a given tag.
        """
        resp = self.call(
            "flickr.photos.search",
            tags=tag,
            # This is so we get the same photos as you see on the "tag" page
            # under "All Photos Tagged XYZ" -- if you click the URL to the
            # full search results, you end up on a page like:
            #
            #     https://flickr.com/search/?sort=interestingness-desc&…
            #
            sort="interestingness-desc",
            extras=",".join(self.extras),
            page=page,
            per_page=per_page,
        )

        return self._parse_collection_of_photos_response(
            find_required_elem(resp, path=".//photos")
        )

    def get_photos_from_flickr_url(self, url: str) -> PhotosFromUrl:
        """
        Given a URL on Flickr.com, return the photos at that URL
        (if possible).

        This can throw a ``NotAFlickrUrl`` and ``UnrecognisedUrl`` exceptions.
        """
        parsed_url = parse_flickr_url(url)

        return self.get_photos_from_parsed_flickr_url(parsed_url)

    def get_photos_from_parsed_flickr_url(
        self, parsed_url: ParseResult
    ) -> PhotosFromUrl:
        """
        Given a URL on Flickr.com that's been parsed with flickr-url-parser,
        return the photos at that URL (if possible).
        """
        if parsed_url["type"] == "single_photo":
            return self.get_single_photo(photo_id=parsed_url["photo_id"])
        elif parsed_url["type"] == "album":
            return self.get_photos_in_album(
                user_url=parsed_url["user_url"],
                album_id=parsed_url["album_id"],
                page=parsed_url["page"],
                per_page=100,
            )
        elif parsed_url["type"] == "user":
            return self.get_public_photos_by_user(
                user_url=parsed_url["user_url"], page=parsed_url["page"], per_page=100
            )
        elif parsed_url["type"] == "gallery":
            return self.get_photos_in_gallery(
                gallery_id=parsed_url["gallery_id"],
                page=parsed_url["page"],
                per_page=100,
            )
        elif parsed_url["type"] == "group":
            return self.get_photos_in_group_pool(
                group_url=parsed_url["group_url"], page=parsed_url["page"], per_page=100
            )
        elif parsed_url["type"] == "tag":
            return self.get_photos_with_tag(
                tag=parsed_url["tag"], page=parsed_url["page"], per_page=100
            )
        else:
            raise TypeError(f"Unrecognised URL type: {parsed_url['type']}")
