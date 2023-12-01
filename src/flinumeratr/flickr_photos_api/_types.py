import datetime
from typing import Literal, TypedDict


class License(TypedDict):
    id: str
    label: str
    url: str | None


class User(TypedDict):
    id: str
    username: str
    realname: str | None
    photos_url: str
    profile_url: str


# Represents the accuracy to which we know a date taken to be true.
#
# See https://www.flickr.com/services/api/misc.dates.html
TakenGranularity = Literal["second", "month", "year", "circa"]


class DateTaken(TypedDict):
    value: datetime.datetime
    granularity: TakenGranularity


class Size(TypedDict):
    label: str
    width: int
    height: int
    media: str
    source: str


class SinglePhoto(TypedDict):
    id: str
    title: str | None
    description: str | None
    owner: User
    date_posted: datetime.datetime
    date_taken: DateTaken | None
    license: License
    url: str
    sizes: list[Size]


class CollectionOfPhotos(TypedDict):
    page_count: int
    total_photos: int
    photos: list[SinglePhoto]


class AlbumInfo(TypedDict):
    owner: User
    title: str


class PhotosInAlbum(CollectionOfPhotos):
    album: AlbumInfo


class GalleryInfo(TypedDict):
    owner_name: str
    title: str


class PhotosInGallery(CollectionOfPhotos):
    gallery: GalleryInfo


class GroupInfo(TypedDict):
    id: str
    name: str


class PhotosInGroup(CollectionOfPhotos):
    group: GroupInfo


PhotosFromUrl = (
    SinglePhoto | CollectionOfPhotos | PhotosInAlbum | PhotosInGallery | PhotosInGroup
)
