#!/usr/bin/env python3

import os
import secrets
import sys

from flask import Flask, flash, render_template, request

from flinumeratr.enumerator import (
    categorise_flickr_url,
    get_photo_data,
    NotAFlickrUrl,
    UnrecognisedUrl,
)
from flinumeratr.flickr_api import FlickrApi, ResourceNotFound


app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex()

try:
    api_key = os.environ["FLICKR_API_KEY"]
except KeyError:
    sys.exit(
        "Could not find Flickr API key! "
        "Please set the FLICKR_API_KEY environment variable and run again."
    )
else:
    api = FlickrApi(api_key=api_key)


@app.template_filter()
def image_at(sizes, desired_size):
    """
    Given a list of image sizes from the Flickr API, return the source URL of
    the desired size.
    """
    # TODO: Make more rigorous.  This function is very basic, and will throw
    # a StopIteration exception if the size isn't found.
    #
    # It would be better if it had an awareness of the sizes that the Flickr API
    # might return, so it could
    return next(s["source"] for s in sizes if s["label"] == desired_size)


@app.template_filter()
def example_url(url):
    display_url = url.replace("https://www.flickr.com", "").replace(
        "https://flickr.com", ""
    )
    return f'<li><a href="/images?flickr_url={url}">{display_url}</a></li>'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/images")
def images():
    url = request.args["flickr_url"]
    page = int(request.args.get("page", "1"))

    try:
        categorised_url = categorise_flickr_url(url)
    except UnrecognisedUrl:
        flash(f"Unable to find any photos at <span class='user_input'>{url}</span>")
        return render_template("error.html", flickr_url=url)
    except NotAFlickrUrl:
        flash(f"The URL <span class='user_input'>{url}</span> isn’t on Flickr.com")
        return render_template("error.html", flickr_url=url)

    category_label = {
        "single_photo": "a photo",
        "photoset": "an album",
        "people": "a person",
        "group": "a group",
        "galleries": "a gallery",
    }[categorised_url["type"]]

    try:
        photos = get_photo_data(api, categorised_url=categorised_url, page=page)
    except ResourceNotFound:
        flash(
            f"Unable to find {category_label} at <span class='user_input'>{url}</span>"
        )
        return render_template("error.html", flickr_url=url)
    except Exception as e:
        flash(f"Boom! Something went wrong: {e}")
        return render_template("error.html", flickr_url=url, error=e)
    else:
        return render_template("images.html", data={**categorised_url, **photos}, label=category_label)


def main():
    app.run(debug=True)
