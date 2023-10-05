# flinumeratr

This is a toy to help you pull photos out of Flickr.
You enter a Flickr URL, and it shows you a list of photos that can be viewed at that URL:
This includes:

*   A single photo, such as [/photos/schlesinger_library/13270291833](https://flinumeratr.glitch.me/see_photos?flickr_url=https://www.flickr.com/photos/schlesinger_library/13270291833)
*   An album, like
[/photos/aljazeeraenglish/albums/72157626164453131](https://flinumeratr.glitch.me/see_photos?flickr_url=https://www.flickr.com/photos/aljazeeraenglish/albums/72157626164453131)
*   A member's photo stream, for example [/people/blueminds/](https://flinumeratr.glitch.me/see_photos?flickr_url=https://www.flickr.com/people/blueminds/)

<img src="screenshot.jpg" alt="Screenshot of flinumeratr. It's a web app with a single input field at the top, into which somebody has entered a Flickr URL. Below the input form is a purple box explaining that this URL shows the photos in a gallery about celebrating Hispanic Heritage Month, and then two photos from the gallery.">

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
