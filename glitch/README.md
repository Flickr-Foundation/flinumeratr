When we first created Flinumeratr, it was deployed as a Glitch app at <https://flinumeratr.glitch.me>

We later moved it to <https://www.flickr.org/tools/flinumeratr/>, so that everything was available on the `flickr.org` domain.
This also allowed us to upgrade a modern version of Python (Glitch was only running EOL Python 3.7 at the time).

This is a tiny app that just redirects requests from Glitch to `flickr.org`.

The app is manually deployed into a Glitch account which Alex logs into with their Flickr Google address.
