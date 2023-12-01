import os
import secrets
import sys

from flask import Flask, flash, redirect, render_template, request, url_for
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
        return render_template(
            "see_photos.html",
            flickr_url=flickr_url,
            parsed_url=parsed_url,
            photo_data=photo_data,
            label=category_label,
        )
