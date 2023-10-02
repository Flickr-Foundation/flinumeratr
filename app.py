#!/usr/bin/env python3

from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
    
    
@app.route("/images")
def images():
    url = request.args['flickr_url']
    return render_template("images.html", url=url)
    

if __name__ == '__main__':
    app.run(debug=True)