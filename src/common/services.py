import logging
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter, Retry

logger = logging.getLogger(__name__)

CLIENT_PROTOCOL = "https"
CLIENT_DOMAIN = "jsonplaceholder.typicode.com"


class FakeApiRequestsHandler:
    """
    Base class to handle REST API requests to a generic endpoint.

    Child classes should implement `list_items`.
    """

    API_ENDPOINT: str = f"{CLIENT_PROTOCOL}://{CLIENT_DOMAIN}"

    def __init__(self, endpoint: Optional[str] = None) -> None:
        """
        Initialize the API request handler with a session that has retries.
        """
        self.api_endpoint: str = endpoint or self.API_ENDPOINT
        self.session: requests.Session = self._create_session()

    def _create_session(self) -> requests.Session:
        """
        Create a requests session with a retry strategy.
        """
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 503, 504),
            allowed_methods=frozenset(["GET"]),
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _fetch_request_data(self, url: str, **kwargs) -> Optional[requests.Response]:
        """
        Make a GET request to the API and return the response or None if failed.
        """
        try:
            response = self.session.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as error:
            logger.error(f"API request to {url} failed: {error}")
            return None

    def _list_from_endpoint(self, path: str) -> List[Dict[str, Any]]:
        """
        Helper to fetch a list of items from a specific API path.

        Logs a warning if no data is retrieved.
        """
        url = f"{self.api_endpoint}/{path}"
        response = self._fetch_request_data(url)
        if not response:
            logger.warning("No data retrieved from %s", url)
            return []
        return response.json()

    def list_items(self) -> List[Dict[str, Any]]:
        """
        Child classes must implement this to fetch list of items.
        """
        raise NotImplementedError("list_items must be implemented in child classes.")
