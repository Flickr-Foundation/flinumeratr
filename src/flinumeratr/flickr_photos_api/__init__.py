from .api import FlickrPhotosApi
from .exceptions import FlickrApiException, ResourceNotFound, LicenseNotFound
from ._types import (
    License,
    User,
    TakenGranularity,
    DateTaken,
    Size,
    SafetyLevel,
    SinglePhoto,
    CollectionOfPhotos,
    PhotosFromUrl,
    PhotosInAlbum,
    PhotosInGallery,
    PhotosInGroup,
    AlbumInfo,
    GalleryInfo,
    GroupInfo,
)


__version__ = "1.1.0"


__all__ = [
    "FlickrPhotosApi",
    "FlickrApiException",
    "ResourceNotFound",
    "LicenseNotFound",
    "License",
    "User",
    "TakenGranularity",
    "DateTaken",
    "Size",
    "SafetyLevel",
    "SinglePhoto",
    "CollectionOfPhotos",
    "PhotosFromUrl",
    "PhotosInAlbum",
    "PhotosInGallery",
    "PhotosInGroup",
    "AlbumInfo",
    "GalleryInfo",
    "GroupInfo",
    "__version__",
]
