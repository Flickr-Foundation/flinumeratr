#!/usr/bin/env python3

import os

from flask import Flask, render_template, request

from flinumeratr.enumerator import categorise_flickr_url
from flinumeratr.flickr_api import FlickrApi, get_single_photo_info


app = Flask(__name__)

api = FlickrApi(api_key=os.environ['FLICKR_API_KEY'])


@app.route("/")
def index():
    return render_template("index.html")
    
    
@app.route("/images")
def images():
    url = request.args['flickr_url']
    
    categorised_url = categorise_flickr_url(url)
    
    if categorised_url['type'] == 'single_photo':
        from pprint import pprint; pprint(categorised_url)
        from pprint import pprint; pprint(
            get_single_photo_info(api, photo_id=categorised_url['photo_id'])
        )
    
    return render_template("images.html", url=url)
    

def main():
    app.run(debug=True)
