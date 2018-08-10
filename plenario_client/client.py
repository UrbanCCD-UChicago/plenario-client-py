import config
import requests
from plenario_response.response import PlenarioResponse

DEFAULT_API_URL = config.API_URL


class PlenarioClient:

    def __init__(self, api_url: str=DEFAULT_API_URL):
        self.api_url: str = api_url
        self.session: requests.Session = requests.Session()
        self.response: requests.Response = None

    def _get_url(self, url: str) -> PlenarioResponse:
        self.response = self.session.get(url)
        return PlenarioResponse(self.response.json(), self.session)

    def get_dataset(self, dataset_slug: str) -> PlenarioResponse:
        self.response = self.session.get(self.api_url + dataset_slug)
        return PlenarioResponse(self.response.json(), self.session)
