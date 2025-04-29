"""
Tests for `flinumeratr.filters`.
"""

from datetime import datetime

from flickr_api.models import DateTaken
import pytest

from flinumeratr.filters import render_date_taken


@pytest.mark.parametrize(
    ["date_taken", "expected_output"],
    [
        # Based on https://www.flickr.com/photos/184374196@N07/53069446440
        (
            {
                "granularity": "second",
                "value": datetime(2023, 2, 20, 23, 31, 31),
            },
            "on February 20, 2023",
        ),
        # Based on https://www.flickr.com/photos/schlesinger_library/13270291833/
        (
            {
                "granularity": "second",
                "value": datetime(2014, 3, 7, 11, 44, 16),
            },
            "on March 7, 2014",
        ),
        # Based on https://www.flickr.com/photos/normko/361850789
        (
            {
                "granularity": "month",
                "value": datetime(1970, 3, 1, 0, 0, 0),
            },
            "in March 1970",
        ),
        # Based on https://www.flickr.com/photos/nationalarchives/5240741057
        (
            {
                "granularity": "year",
                "value": datetime(1950, 1, 1, 0, 0, 0),
            },
            "sometime in 1950",
        ),
        # Based on https://www.flickr.com/photos/nlireland/6975991819
        (
            {
                "granularity": "circa",
                "value": datetime(1910, 1, 1, 0, 0, 0),
            },
            "circa 1910",
        ),
    ],
)
def test_render_date_taken(date_taken: DateTaken, expected_output: str) -> None:
    assert render_date_taken(date_taken) == expected_output
