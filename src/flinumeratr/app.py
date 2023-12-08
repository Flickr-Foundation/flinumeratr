import os
import secrets
import sys
import requests  # api is using httpx though

from flask import Flask, flash, redirect, render_template, request, url_for, Response, jsonify
from flickr_url_parser import (
    parse_flickr_url,
    NotAFlickrUrl,
    UnrecognisedUrl,
)
import humanize

from .filters import render_date_taken
from .flickr_photos_api import FlickrPhotosApi, ResourceNotFound, Size as PhotoSize
from ._types import ViewResponse


app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex()

app.add_template_filter(render_date_taken)

try:
    api_key = os.environ["FLICKR_API_KEY"]
except KeyError:  # pragma: no cover
    sys.exit(
        "Could not find Flickr API key! "
        "Please set the FLICKR_API_KEY environment variable and run again."
    )
else:
    api = FlickrPhotosApi(
        api_key=api_key,
        user_agent="Flinumeratr/1.1.0 (https://github.com/flickr-foundation/flinumeratr; hello@flickr.org)",
    )


@app.template_filter()
def image_at(sizes: list[PhotoSize], desired_size: str) -> str:
    """
    Given a list of sizes of Flickr photo, return the source of
    the desired size.
    """
    sizes_by_label = {s["label"]: s for s in sizes}

    # Flickr has a published list of possible sizes here:
    # https://www.flickr.com/services/api/misc.urls.html
    #
    # If the desired size isn't available, that means one of two things:
    #
    #   1.  The owner of this photo has done something to restrict downloads
    #       of their photo beyond a certain size.  But CC-licensed photos
    #       are always available to download, so that's not an issue for us.
    #   2.  This photo is smaller than the size we've asked for, in which
    #       case we fall back to Original as the largest possible size.
    #
    try:
        return sizes_by_label[desired_size]["source"]
    except KeyError:  # pragma: no cover
        return sizes_by_label["Original"]["source"]


@app.template_filter()
def example_url(url: str) -> str:
    display_url = url.replace("https://www.flickr.com", "").replace(
        "https://flickr.com", ""
    )

    app_url = url_for("see_photos", flickr_url=url)

    return f'<li><a href="{app_url}">{display_url}</a></li>'


@app.template_filter()
def intcomma(n: int) -> str:
    return humanize.intcomma(n)


@app.route("/")
def index() -> ViewResponse:
    return render_template("index.html")


@app.route("/see_photos")
def see_photos() -> ViewResponse:
    try:
        flickr_url = request.args["flickr_url"]
    except KeyError:
        return redirect(url_for("index"))

    try:
        parsed_url = parse_flickr_url(flickr_url)
    except UnrecognisedUrl:
        flash(
            f"There are no photos to show at <span class='user_input'>{flickr_url}</span>"
        )
        return render_template("error.html", flickr_url=flickr_url)
    except NotAFlickrUrl:
        flash(
            f"<span class='user_input'>{flickr_url}</span> doesn’t live on Flickr.com"
        )
        return render_template("error.html", flickr_url=flickr_url)

    category_label = {
        "single_photo": "a photo",
        "photoset": "an album",
        "people": "a person",
        "group": "a group",
        "galleries": "a gallery",
        "tags": "a tag",
    }.get(parsed_url["type"], "a " + parsed_url["type"])

    try:
        photo_data = api.get_photos_from_parsed_flickr_url(parsed_url=parsed_url)
    except ResourceNotFound:
        flash(
            f"Unable to find {category_label} at <span class='user_input'>{flickr_url}</span>"
        )
        return render_template("error.html", flickr_url=flickr_url)
    except Exception as e:  # pragma: no cover
        flash(f"Boom! Something went wrong: {e}")
        return render_template("error.html", flickr_url=flickr_url, error=e)
    else:
        if request.args.get("iiif", None) is None:
            return render_template(
                "see_photos.html",
                flickr_url=flickr_url,
                parsed_url=parsed_url,
                photo_data=photo_data,
                label=category_label,
            )
        elif request.args.get("raw", None) is not None:
            return photo_data
        else:
            canvases = make_canvases(photo_data)
            manifest_id = f'{url_for("see_photos", _external=True)}?flickr_url={flickr_url}&iiif=true'
            manifest = make_manifest(
                manifest_id, canvases,
                photo_data=photo_data, label=category_label, flickr_url=flickr_url, parsed_url=parsed_url)
            return jsonify(manifest)


"""
IIIF Image API routes
"""


@app.route('/iiif/image/<photo_id>')
def image_info(photo_id):
    return redirect(url_for("info_json_response", photo_id=photo_id, _external=True))


@app.route('/iiif/image/v2/<photo_id>')
def image_info_v2(photo_id):
    return redirect(url_for("info_json_response_v2", photo_id=photo_id, _external=True))


@app.route('/iiif/image/<photo_id>/info.json')
def info_json_response(photo_id):
    # photo = get_api_object("flickr.photos.getInfo", photo_id=photo_id)
    # The Original size may or may not be present in the sizes list
    sizes = get_non_square_sizes(photo_id)
    largest = list(sizes.values())[-1]
    info_json = {
        "@context": "http://iiif.io/api/image/3/context.json",
        "id": url_for("image_info", photo_id=photo_id, _external=True),
        "type": "ImageService3",
        "protocol": "http://iiif.io/api/image",
        "profile": "level0",
        "width": int(largest["width"]),
        "height": int(largest["height"]),
        "sizes": []
    }
    for size in sizes.values():
        info_json["sizes"].append({
            "width": size["width"],
            "height": size["height"]
        })

    # Rights - this doesn't map to IIIF cleanly but better than nothing for now
    # Need to handle Flickr All Rights Reserved
    # license_url = get_license_url(photo["photo"].get("license", None))
    # if license_url:
    #     info_json["rights"] = license_url

    return jsonify(info_json)


@app.route('/iiif/image/v2/<photo_id>/info.json')
def info_json_response_v2(photo_id):
    # photo = get_api_object("flickr.photos.getInfo", photo_id=photo_id)
    # The Original size may or may not be present in the sizes list
    sizes = get_non_square_sizes(photo_id)
    largest = list(sizes.values())[-1]
    info_json = {
        "@context": "http://iiif.io/api/image/2/context.json",
        "@id": url_for("image_info_v2", photo_id=photo_id, _external=True),
        "protocol": "http://iiif.io/api/image",
        "profile": ["http://iiif.io/api/image/2/level0.json"],
        "width": int(largest["width"]),
        "height": int(largest["height"]),
        "sizes": []
    }
    for size in sizes.values():
        info_json["sizes"].append({
            "width": size["width"],
            "height": size["height"]
        })

    return jsonify(info_json)


@app.route('/iiif/image/<photo_id>/full/<wh>/0/default.jpg')
@app.route('/iiif/image/v2/<photo_id>/full/<wh>/0/default.jpg')
def image_api_request(photo_id, wh):
    sizes = get_non_square_sizes(photo_id)
    if wh == "max":
        size = list(sizes.values())[-1]
    else:
        width = int(wh.split(',')[0])
        size = sizes.get(width, None)
    if size is not None:
        r = Response(response=requests.get(size["source"]).content, status=200)
        r.headers["Content-Type"] = "image/jpg"
        return r
    Flask.abort(404)


def get_non_square_sizes(photo_id):
    # might be worth memoizing by photo_id?
    # TODO - use secret to get larger sizes when available
    photo = api.get_single_photo(photo_id=photo_id)
    return {int(s["width"]): s for s in photo["sizes"] if "quare" not in s["label"]}


"""
IIIF Presentation API
"""


def make_manifest(manifest_id, canvases, photo_data, label, flickr_url, parsed_url):
    description = "Unknown url type"
    total_photos = photo_data.get("total_photos", 0)
    if parsed_url["type"] == "user":
        user = photo_data.photos[0].owner
        description = f'<p>This IIIF Manifest shows the photos taken by <a href="{user.profile_url}">{user.realname or user.username}</a>, who has posted {total_photos} photos</p>'
    elif parsed_url["type"] == "album":
        username = photo_data["album"]["owner"].get("realname", None) or photo_data["album"]["owner"].get("username", "???")
        description = f'<p>This IIIF Manifest shows the photos in the <a href="{flickr_url}">{photo_data["album"]["title"]}</a> album, which was created by <a href="{url_for('see_photos', flickr_url=photo_data["album"]["owner"]["profile_url"])}">{username}</a>.It contains {total_photos} photos</p>'
    elif parsed_url["type"] == "group":
        description = f'<p>This IIIF Manifest shows the photos in the <a href="{flickr_url}">{photo_data["group"]["name"]}</a> group pool, which contains {total_photos}&nbsp;photos.</p>'
    elif parsed_url["type"] == "gallery":
        description = f'<p>This IIIF Manifest shows the photos in the <a href="{flickr_url}">{photo_data["gallery"]["title"]}</a> gallery, which contains {total_photos}&nbsp;photos.</p>'
    elif parsed_url["type"] == "tag":
        description = f'<p>This IIIF Manifest shows photos tagged with <a href="{flickr_url}">{ parsed_url["tag"] }</a>.</p>'
    elif parsed_url["type"] == "single_photo":
        description = f'<p>This IIIF Manifest is <a href="{flickr_url}">a single photo</a> on Flickr.</p>'
    return {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": manifest_id,
        "type": "Manifest",
        "label": [{"en": [label]}],
        "metadata": [{"label": {"en": ["Description"]}, "value": {"en": [description]}}],
        "items": canvases
    }


def make_canvases(photo_data):
    # TODO - use secret to get larger sizes when available; this is limited to non-authenticated API calls atm
    # We're also assuming url_l, width_l and height_l exist, and they may not.
    # This can become MUCH more robust.
    if photo_data.get("id", None) and photo_data.get("sizes", None):
        # this is a single photo
        photo_data = {"photos": [photo_data]}
    canvases = []
    for photo in photo_data["photos"]:
        photo_id = photo["id"]
        canvas_id = url_for("canvas", photo_id=photo_id, _external=True)
        size_info = get_sizes_from_photo(photo)
        canvas_with_image = {
            "id": canvas_id,
            "type": "Canvas",
            "width": size_info["largest"]["width"],
            "height": size_info["largest"]["height"],
            "label": {"en": [photo["title"]]},
            "items": [
                {
                    "id": f"{canvas_id}/annopage",
                    "type": "AnnotationPage",
                    "items": [
                        {
                            "id": f"{canvas_id}/annopage/anno",
                            "type": "Annotation",
                            "motivation": "painting",
                            "body": {
                                "id": size_info["largest"]["url"],
                                "type": "Image",
                                "format": "image/jpeg",
                                "service": [
                                    {
                                        "id": url_for("image_info", photo_id=photo_id, _external=True),
                                        "type": "ImageService3",
                                        "profile": "level0"
                                    }
                                ],
                                "width": size_info["largest"]["width"],
                                "height": size_info["largest"]["height"],
                            },
                            "target": canvas_id
                        }
                    ]
                }
            ]
        }
        thumb_image = size_info.get("thumb", None)
        if thumb_image is not None:
            canvas_with_image["thumbnail"] = [{
                "id": thumb_image["url"],
                "type": "Image",
                "format": "image/jpg",
                "width": thumb_image["width"],
                "height": thumb_image["height"],
            }]
        canvases.append(canvas_with_image)
    return canvases


def get_sizes_from_photo(photo):
    # Using the photo object returned in a collection of photos, rather than making any new calls
    # This is where we would want to list all possible available sizes, even secret ones.
    # for now, it's enough to get _something_ out.
    size_info = {
        "largest": None,  # the biggest one we find regardless of suffix
        "thumb": None,
        "square": None,
        "all": {}
    }
    # This is mostly unnecessary - the flinumerator API does this for me
    # TODO - tidy this up
    for entry in photo["sizes"]:
        suffix = entry["source"].split("_")[1]
        size = {
            "width": entry["width"],
            "height": entry["height"],
            "url": entry["source"],
            "suffix": suffix
        }
        if suffix == "sq":
            # don't include the square one in the list
            size_info["square"] = size
        else:
            size_info["all"]["suffix"] = size
            # but do include the thumbnail
            if suffix == "t":
                size_info["thumb"] = size
    size_info["largest"] = max(size_info["all"].values(), key=lambda x: x["width"])
    return size_info


@app.route('/iiif/canvas/<photo_id>')
def canvas(photo_id):
    Flask.abort(404)
