import typing

from flickr_photos_api import SinglePhoto, User


class CollectionOfPhotos(typing.TypedDict):
    photos: list[SinglePhoto]

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
    SinglePhoto | CollectionOfPhotos | PhotosInAlbum | PhotosInGallery | PhotosInGroup
)
