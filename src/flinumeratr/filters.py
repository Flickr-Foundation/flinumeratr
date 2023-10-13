class TakenDateGranularity:
    """
    Named constants for Flickr "Taken date" granularity.

    See https://www.flickr.com/services/api/misc.dates.html
    """

    Day = "0"
    Month = "4"
    Year = "6"
    Circa = "8"


def render_date_taken(date_taken):
    if date_taken["unknown"]:
        return
    elif date_taken["granularity"] == TakenDateGranularity.Day:
        return f"on {date_taken['value'].strftime('%B %-d, %Y')}"
    elif date_taken["granularity"] == TakenDateGranularity.Month:
        return f"in {date_taken['value'].strftime('%B %Y')}"
    elif date_taken["granularity"] == TakenDateGranularity.Year:
        return f"sometime in {date_taken['value'].strftime('%Y')}"
    elif date_taken["granularity"] == TakenDateGranularity.Circa:
        return f"circa {date_taken['value'].strftime('%Y')}"
    else:
        raise ValueError(f"Unrecognised granularity: {date_taken['granularity']}")
