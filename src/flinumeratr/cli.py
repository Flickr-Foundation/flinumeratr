import argparse  # pragma: no cover


def main() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(
        prog="flinumeratr",
        description="Run a local version of flinumeratr, a toy to help you pull photos out of Flickr.",
    )

    parser.add_argument("--port", help="the port to bind to", type=int, default=5000)
    parser.add_argument("--host", default="127.0.0.1", help="the interface to bind to")
    parser.add_argument("--debug", action="store_true", help="run in debug mode")

    args = parser.parse_args()

    from flinumeratr.app import app

    app.run(debug=args.debug, port=args.port, host=args.host)
