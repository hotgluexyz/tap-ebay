"""Ebay tap class."""

from typing import List

from hotglue_tap_sdk import Tap, Stream
from hotglue_tap_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_ebay.streams import (
    OrdersStream,
)
STREAM_TYPES = [
    OrdersStream,
]


class TapEbay(Tap):
    """Ebay tap class."""
    name = "tap-ebay"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "refresh_token",
            th.StringType,
            required=True,
        ),
        th.Property(
            "client_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]

if __name__ == "__main__":
    TapEbay.cli()