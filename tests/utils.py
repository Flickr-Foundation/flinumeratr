import datetime
import json
import os
from typing import Any, Literal, TypedDict, TypeVar

from pydantic import ConfigDict, TypeAdapter


T = TypeVar("T")

EncodedDate = TypedDict(
    "EncodedDate", {"type": Literal["datetime.datetime"], "value": str}
)


class DatetimeDecoder(json.JSONDecoder):
    """
    A custom JSON decoder that supports native datetimes.

        >>> json.loads(
        ...     '{"t": {"type": "datetime.datetime", "value": "2001-02-03T04:05:06"}}',
        ...     cls=DatetimeDecoder)
        {'t': datetime.datetime(2001, 2, 3, 4, 5, 6)}

    """

    def __init__(self) -> None:
        super().__init__(object_hook=self.dict_to_object)

    def dict_to_object(self, d: dict[str, Any]) -> dict[str, Any] | datetime.datetime:
        if d.get("type") == "datetime.datetime":
            return datetime.datetime.fromisoformat(d["value"])
        else:
            return d


def validate_typeddict(t: Any, model: type[T]) -> T:
    """
    Check that some data matches a TypedDict.

    We use this to check that the structured data we receive
    from Wikimedia matches our definitions, so we can use it
    in type-checked Python.

    See https://stackoverflow.com/a/77386216/1558022
    """
    model.__pydantic_config__ = ConfigDict(extra="forbid")  # type: ignore
    TypedDictValidator = TypeAdapter(model)
    return TypedDictValidator.validate_python(t, strict=True)


def get_typed_fixture(path: str, model: type[T]) -> T:
    """
    Read a JSON fixture from the ``tests/fixtures`` directory.

    This function will validate that the JSON fixture matches the
    specified model.
    """
    with open(os.path.join("tests/fixtures/api_responses", path)) as f:
        return validate_typeddict(json.load(f, cls=DatetimeDecoder), model)
