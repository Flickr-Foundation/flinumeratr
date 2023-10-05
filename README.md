# flinumeratr

This is a project that takes a URL from Flickr.com, and shows a list of images that can be viewed at that URL.
This includes:

*   URLs for individual photos (e.g. <https://www.flickr.com/photos/coast_guard/32812033543>)
*   URLs for albums (e.g. <https://www.flickr.com/photos/cat_tac/albums/72157666833379009>)
*   URLs for a person's profile (e.g. <https://www.flickr.com/people/blueminds/>)

## Usage

You can use flinumeratr by visiting <https://flinumeratr.glitch.me>

## Development

You can set up a local development environment by cloning the repo and installing dependencies:

```console
$ git clone https://github.com/Flickr-Foundation/flinumeratr.git
$ cd flinumeratr
$ python3 -m venv env
$ source env/bin/activate
$ pip install -e .
```

You need [a Flickr API key][key].
Then you can run the app by running `flinumeratr` with your API key passed as an environment variable:

```console
$ FLICKR_API_KEY=<KEY> flinumeratr
```

You can run `flinumeratr --help` to see a few other options.

If you want to run tests, install the dev dependencies and run py.test:

```console
$ source env/bin/activate
$ pip install -r dev_requirements.txt
$ pytest
```

To deploy a new version of flinumeratr, log in to the Glitch app and run the following commands in the Glitch terminal:

```console
$ git pull gh main
$ refresh
```

[key]: https://www.flickr.com/services/api/misc.api_keys.html

## License

This project is dual-licensed as Apache-2.0 and MIT.
