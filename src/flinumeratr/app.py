#!/usr/bin/env python3

import os
import sys

from flask import Flask, render_template, request

from flinumeratr.enumerator import flinumerate
from flinumeratr.flickr_api import FlickrApi


app = Flask(__name__)

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
    return next(s["source"] for s in sizes if s["label"] == desired_size)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/images")
def images():
    url = request.args["flickr_url"]
    page = int(request.args.get("page", "1"))

    return render_template("images.html", data=flinumerate(api, url=url, page=page))


def main():
    app.run(debug=True)
