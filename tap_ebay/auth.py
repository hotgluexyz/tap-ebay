"""Ebay Authentication."""


from hotglue_tap_sdk.authenticators import OAuthAuthenticator, SingletonMeta


PROD_TOKEN_ENDPOINT = "https://api.ebay.com/identity/v1/oauth2/token"
SANDBOX_TOKEN_ENDPOINT = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"

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
        is_sandbox = stream._tap.config.get("is_sandbox", False)
        
        return cls(
            stream=stream,
            config_file=stream._tap.config,
            auth_endpoint=SANDBOX_TOKEN_ENDPOINT if is_sandbox else PROD_TOKEN_ENDPOINT,
            oauth_scopes=None,
        )
