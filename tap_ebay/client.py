"""REST client handling, including EbayStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from hotglue_tap_sdk.helpers.jsonpath import extract_jsonpath
from hotglue_tap_sdk.streams import RESTStream

from tap_ebay.auth import EbayAuthenticator
from datetime import timedelta



class EbayStream(RESTStream):
    """Ebay stream class."""

    url_base = "https://api.ebay.com"
    limit = 200

    @property
    @cached
    def authenticator(self) -> EbayAuthenticator:
        """Return a new authenticator object."""
        return EbayAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        orders = self.parse_response(response)
        if not len(list(orders)):
            return None
        previous_token = previous_token or 0
        return previous_token + self.limit

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["limit"] = self.limit
        if next_page_token:
            params["offset"] = next_page_token
        if self.replication_key:
            start_date = self.get_starting_time(context) + timedelta(seconds=1)
            params["filter"] = f"lastmodifieddate:[{start_date.strftime('%Y-%m-%dT%H:%M:%SZ')}..]"
        return params


