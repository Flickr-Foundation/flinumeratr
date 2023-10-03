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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/images")
def images():
    return render_template(
        "images.html", data=flinumerate(api, url=request.args["flickr_url"])
    )


def main():
    app.run(debug=True)
