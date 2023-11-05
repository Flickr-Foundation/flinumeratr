def render_date_taken(date_taken):
    if date_taken["unknown"]:
        return
    elif date_taken["granularity"] == "second":
        return f"on {date_taken['value'].strftime('%B %-d, %Y')}"
    elif date_taken["granularity"] == "month":
        return f"in {date_taken['value'].strftime('%B %Y')}"
    elif date_taken["granularity"] == "year":
        return f"sometime in {date_taken['value'].strftime('%Y')}"
    elif date_taken["granularity"] == "circa":
        return f"circa {date_taken['value'].strftime('%Y')}"
    else:
        raise ValueError(f"Unrecognised granularity: {date_taken['granularity']}")
