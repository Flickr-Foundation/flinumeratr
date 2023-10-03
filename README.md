# flinumeratr

This is a project that takes a URL from Flickr.com, and shows a list of images that can be viewed at that URL.
This includes:

*   URLs for individual photos (e.g. <https://www.flickr.com/photos/coast_guard/32812033543>)
*   URLs for albums (e.g. <https://www.flickr.com/photos/cat_tac/albums/72157666833379009>)
*   URLs for a person's profile (e.g. <https://www.flickr.com/people/blueminds/>)

## Usage

The tool is still in a very early stage and not deployed anywhere yet.
Watch this space!

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

If you want to run tests, install the dev dependencies and run py.test:

```console
$ source env/bin/activate
$ pip install -r dev_requirements.txt
$ pytest
```

[key]: https://www.flickr.com/services/api/misc.api_keys.html

## License

This project is dual-licensed as Apache-2.0 and MIT.
