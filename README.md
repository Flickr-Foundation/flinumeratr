# flinumeratr

This is a toy to help you pull photos out of Flickr.
You enter a Flickr URL, and it shows you a list of photos that can be viewed at that URL.
This includes:

*   A single photo, such as [/photos/schlesinger_library/13270291833](https://www.flickr.org/tools/flinumeratr/see_photos?flickr_url=https://www.flickr.com/photos/schlesinger_library/13270291833)
*   An album, like
[/photos/aljazeeraenglish/albums/72157626164453131](https://www.flickr.org/tools/flinumeratr?flickr_url=https://www.flickr.com/photos/aljazeeraenglish/albums/72157626164453131)
*   A member's photo stream, for example [/people/blueminds/](https://www.flickr.org/tools/flinumeratr?flickr_url=https://www.flickr.com/people/blueminds/)

<img src="screenshot.jpg" alt="Screenshot of flinumeratr. It's a web app with a single input field at the top, into which somebody has entered a Flickr URL. Below the input form is a purple box explaining that this URL shows the photos in a gallery about celebrating Hispanic Heritage Month, and then two photos from the gallery.">

## Usage

You can use flinumeratr by visiting <https://www.flickr.org/tools/flinumeratr/>

## Development

You can set up a local development environment by cloning the repo and installing dependencies:

```console
$ git clone https://github.com/Flickr-Foundation/flinumeratr.git
$ cd flinumeratr
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -e .
```

You need [a Flickr API key][key].
Then you can run the app by running the Flask app with your API key passed as an environment variable:

```console
$ FLICKR_API_KEY=<KEY> flask --app flinumeratr.app run --debug
```

If you want to run tests, install the dev dependencies and run py.test:

```console
$ source .venv/bin/activate
$ pip install -r dev_requirements.txt
$ coverage run -m pytest tests
$ coverage report
```

To start the server in prod:

```console
$ bash start_prod.sh
```

To restart the server (e.g. if you've changed the code):

```console
$ kill -HUP $(cat flinumeratr.pid)
```

[key]: https://www.flickr.com/services/api/misc.api_keys.html

## License

This project is dual-licensed as Apache-2.0 and MIT.
