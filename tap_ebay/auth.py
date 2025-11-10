"""Ebay Authentication."""


from tkinter import N
from hotglue_tap_sdk.authenticators import OAuthAuthenticator, SingletonMeta


class EbayAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Ebay."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Ebay API."""
        return {
            'refresh_token': self.config["refresh_token"],
            'grant_type': 'refresh_token',
        }
    
    def request_auth(self) -> tuple[str, str]:
        """Return the authentication credentials for the request."""
        return (self.config["client_id"], self.config["client_secret"])

    @classmethod
    def create_for_stream(cls, stream) -> "EbayAuthenticator":
        return cls(
            stream=stream,
            config_file=stream._tap.config,
            auth_endpoint="https://api.ebay.com/identity/v1/oauth2/token",
            oauth_scopes=None,
        )
