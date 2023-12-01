import datetime
import json
import os
from typing import Any, TypeVar, Union


def get_fixture(filename: str) -> Any:
    with open(os.path.join("tests/fixtures/api_responses", filename)) as f:
        return json.load(f)


T = TypeVar("T")


def jsonify(t: T) -> Any:
    """
    Cast a value to/from JSON, suitable for comparison with a JSON fixture.

    The reason we can't just compare directly, e.g.

        assert v == json.load(open("fixture.json"))

    is because some of our objects include ``datetime.datetime`` values,
    which are serialised as strings in the JSON.

    To enable easy comparisons, we need to turn the ``datetime.datetime``
    into strings.  e.g.

        >>> v = {'time': datetime.datetime.now()}
        >>> jsonify(v)
        {'time': '2023-10-20T13:30:45.567888'}

    You still get back a Python object, but now it can be compared to
    a value deserialised from JSON.

    """

    class DatetimeEncoder(json.JSONEncoder):
        def default(self, t: T) -> Union[str, T]:
            if isinstance(t, datetime.datetime):
                return t.isoformat()
            else:  # pragma: no cover
                return t

    return json.loads(json.dumps(t, cls=DatetimeEncoder))
