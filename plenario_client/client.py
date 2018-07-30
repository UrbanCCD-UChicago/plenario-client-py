import config
import requests
from plenario_response.response import PlenarioResponse

DEFAULT_API_URL = config.API_URL

class PlenarioClient:

    def __init__(self, api_url: str=DEFAULT_API_URL):
        self.api_url = api_url
        self.session = requests.Session()
        self.response = None

    def get(self) -> PlenarioResponse:
        self.response = self.session.get(self.api_url)
        return PlenarioResponse(self.response.json())
