from datetime import datetime
import typing

from flickr_photos_api import DateTaken, License, User


class Photo(typing.TypedDict):
    # URL to the photo description page
    url: str

    # URL to a photo size, i.e. the JPEG file
    image_url: str

    # title of the photo
    title: str | None

    # URL to the owner's profile page
    owner_url: str

    # Name of the owner
    owner_name: str

    # When was the photo taken/uploaded to Flickr?
    date_taken: DateTaken | None
    date_posted: datetime

    # What license does the photo have?
    license: License


class CollectionOfPhotos(typing.TypedDict):
    photos: list[Photo]

    # Note: there are no parameters named like this in the Flickr API;
    # these names were chosen to match parameters that do exist like
    # `count_views` or `count_comments`.
    count_pages: int
    count_photos: int


class AlbumInfo(typing.TypedDict):
    owner: User
    title: str


class PhotosInAlbum(CollectionOfPhotos):
    album: AlbumInfo


class GalleryInfo(typing.TypedDict):
    owner_name: str
    title: str


class PhotosInGallery(CollectionOfPhotos):
    gallery: GalleryInfo


class GroupInfo(typing.TypedDict):
    id: str
    name: str


class PhotosInGroup(CollectionOfPhotos):
    group: GroupInfo


PhotosFromUrl = (
    Photo | CollectionOfPhotos | PhotosInAlbum | PhotosInGallery | PhotosInGroup
)
