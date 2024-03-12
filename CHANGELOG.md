# CHANGELOG

## v1.2.0 - 2024-03-12

*   Remove the custom CLI; just invoke the dev server using the Flask CLI.

## v1.1.0 - 2023-10-13

*   Add support for finding photos at Flickr short URLs, including:

    - Single photo URLs, like https://flic.kr/p/2p4QbKN
    - Gallery URLs, like https://flic.kr/y/2Xry4Jt
    - Album URLs, like https://flic.kr/s/aHsjybZ5ZD
    - People URLs, like https://flic.kr/ps/ZVcni

*   Render "date taken" with the correct level of granularity.
    For example, if somebody has marked their photo as "circa 1910" or "taken in March 2020" on Flickr.com, this is now rendered correctly in Flinumeratr.

    Previously it would incorrectly render a full day/month/year date.

## v1.0.0 - 2023-10-06

Initial release, as [publicised in an article on flickr.org](https://www.flickr.org/introducing-flinumeratr-our-first-toy/).

At this point flinumeratr is considered "largely complete" -- we may do bug fixes and refactoring, but it's no longer the main focus of our attention.

