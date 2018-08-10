from plenario_response.meta import Meta
from plenario_response.data import Data
import requests


class PlenarioResponse:

    def __init__(self, json_payload: dict, session: requests.Session=None):
        self.payload: dict = json_payload
        self._meta: Meta = Meta(self.payload.get('meta'))
        self._data: Data = Data(self.payload.get('data'))
        self._session = session

    def __iter__(self):
        while self.meta.next_page_link:
            response = self._session.get(self.meta.next_page_link)
            next_page = PlenarioResponse(response.json(), self._session)
            yield self
            self = next_page
        else:
            yield self
            raise StopIteration

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def data(self) -> Data:
        return self._data
