import config
import requests
from plenario_response.response import PlenarioResponse


class PlenarioClient(object):

    def __init__(self, api_url=None):
        if api_url is None:
            api_url = config.API_URL
        self.api_url = api_url
        self.session = requests.Session()
        self.response = None

    def get(self):
        self.response = self.session.get(self.api_url)
        return PlenarioResponse(self.response.json())
