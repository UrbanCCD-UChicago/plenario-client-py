from abc import ABC

from requests import Session

from .errors import ApiError
from .filters import F


class ResponseHandler(ABC):

    @classmethod
    def from_api_payload(cls, payload: dict, client: 'Client'=None):
        raise NotImplementedError


class ClientBase(ABC):

    DEFAULT_SCHEME: str = 'https'
    DEFAULT_HOSTNAME: str = 'plenar.io'
    DEFAULT_VERSION: str = 'v2'

    ENDPOINT: str = ''

    def __init__(self, scheme: str=DEFAULT_SCHEME, hostname: str=DEFAULT_HOSTNAME, version: str=DEFAULT_VERSION):
        self.base_path = f'{scheme}://{hostname}/api/{version}/{self.ENDPOINT}'
        self.session = Session()

    def _send_request(self, url: str, parse_as: ResponseHandler, params: F=None):
        if isinstance(params, F):
            params = params.to_query_params()

        response = self.session.get(url, params=params)
        payload = response.json()

        if 'error' in payload:
            raise ApiError(payload['error'])

        return parse_as.from_api_payload(client=self, payload=payload)
