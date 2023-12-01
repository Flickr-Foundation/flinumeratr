import datetime

import pytest

from flinumeratr.filters import render_date_taken
from flinumeratr.flickr_photos_api import DateTaken


@pytest.mark.parametrize(
    ["date_taken", "expected_output"],
    [
        # Based on https://www.flickr.com/photos/184374196@N07/53069446440
        (
            {
                "granularity": "second",
                "value": datetime.datetime(2023, 2, 20, 23, 31, 31),
            },
            "on February 20, 2023",
        ),
        # Based on https://www.flickr.com/photos/schlesinger_library/13270291833/
        (
            {
                "granularity": "second",
                "value": datetime.datetime(2014, 3, 7, 11, 44, 16),
            },
            "on March 7, 2014",
        ),
        # Based on https://www.flickr.com/photos/normko/361850789
        (
            {
                "granularity": "month",
                "value": datetime.datetime(1970, 3, 1, 0, 0, 0),
            },
            "in March 1970",
        ),
        # Based on https://www.flickr.com/photos/nationalarchives/5240741057
        (
            {
                "granularity": "year",
                "value": datetime.datetime(1950, 1, 1, 0, 0, 0),
            },
            "sometime in 1950",
        ),
        # Based on https://www.flickr.com/photos/nlireland/6975991819
        (
            {
                "granularity": "circa",
                "value": datetime.datetime(1910, 1, 1, 0, 0, 0),
            },
            "circa 1910",
        ),
        # Based on https://www.flickr.com/photos/140375060@N02/25868667441/
        (None, None),
    ],
)
def test_render_date_taken(date_taken: DateTaken | None, expected_output: str) -> None:
    assert render_date_taken(date_taken) == expected_output


def test_render_date_taken_fails_with_unrecognised_granularity() -> None:
    with pytest.raises(ValueError):
        render_date_taken(
            date_taken={
                "granularity": -1,  # type: ignore
                "value": datetime.datetime.now(),
                "unknown": False,
            }
        )
