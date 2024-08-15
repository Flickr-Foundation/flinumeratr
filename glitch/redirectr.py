from flask import Flask, Response, redirect, request

app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path: str) -> Response:
    if request.query_string:
        return redirect(
            "https://www.flickr.org/tools/flinumeratr/"
            + path
            + "?"
            + request.query_string.decode("utf8")
        )
    else:
        return redirect("https://www.flickr.org/tools/flinumeratr/" + path)
