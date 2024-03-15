import logging
import requests

from typing import List, Dict

logger = logging.getLogger(__name__)


CLIENT_PROTOCOL = 'https'
CLIENT_DOMAIN = 'jsonplaceholder.typicode.com'


class FakeApiRequestsHandler(object):
    """Generic Strategy class that defines strategies for chield classes."""

    API_ENDPOINT = f"{CLIENT_PROTOCOL}://{CLIENT_DOMAIN}"

    def _fetch_request_data(
            self, url: str, **kwargs: Dict) -> requests.Response:
        """Generic function to make a REST API request."""

        try:
            response = requests.get(url, **kwargs)      
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error(f"API request failed: {error}")
            return None

        return response

    def get_list_request(self) -> List[Dict]:
        """Method must be implemented in chield classes."""

        raise NotImplementedError()


class PostsRequestHandler(FakeApiRequestsHandler):
    """Strategy class that implements strategies for the parent class."""

    def get_list_request(self) -> List[Dict]:
        """Retrieve all posts from fake placeholder api."""

        response = self._fetch_request_data(f'{self.API_ENDPOINT}/posts')
        return [] if not response else response.json()


class CommentsRequestHandler(FakeApiRequestsHandler):
    """Strategy class that implements strategies for the parent class."""

    def get_list_request(self) -> List[Dict]:
        """Retrieve all comments from fake placeholder api."""

        response = self._fetch_request_data(f'{self.API_ENDPOINT}/comments')

        return [] if not response else response.json()
