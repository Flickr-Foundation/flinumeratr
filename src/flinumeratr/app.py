import os
import secrets
import sys

from flask import Flask, flash, redirect, render_template, request, url_for
from flickr_photos_api import FlickrApi, ResourceNotFound, Size as PhotoSize
from flickr_url_parser import (
    parse_flickr_url,
    NotAFlickrUrl,
    UnrecognisedUrl,
)
import humanize
import werkzeug

from . import __version__
from .filters import render_date_taken
from .flickr_api import get_photos_from_flickr_url


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
    api = FlickrApi.with_api_key(
        api_key=api_key,
        user_agent=f"Flinumeratr/{__version__} (https://github.com/flickr-foundation/flinumeratr; hello@flickr.org)",
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
    #       case we fall back to the largest possible size.
    #
    try:
        return sizes_by_label[desired_size]["source"]
    except KeyError:  # pragma: no cover
        return max(sizes, key=lambda s: s["width"] or 0)["source"]


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
def homepage() -> str:
    """
    The Flinumeratr homepage.
    """
    return render_template("homepage.html")


@app.route("/see_photos")
def see_photos() -> str | werkzeug.Response:
    try:
        flickr_url = request.args["flickr_url"]
    except KeyError:
        return redirect(url_for("homepage"))

    # If the user enters an empty string, just redirect them back to
    # the homepage.
    if not flickr_url:
        return redirect(url_for("homepage"))

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
        "album": "an album",
        "user": "a person",
        "group": "a group",
        "gallery": "a gallery",
        "tag": "a tag",
    }[parsed_url["type"]]

    try:
        photo_data = get_photos_from_flickr_url(api, parsed_url)
    except ResourceNotFound:
        flash(
            f"Unable to find {category_label} at <span class='user_input'>{flickr_url}</span>"
        )
        return render_template("error.html", flickr_url=flickr_url)
    except Exception as e:  # pragma: no cover
        raise
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
