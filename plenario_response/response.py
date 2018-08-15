from plenario_response.meta import Meta
from plenario_response.data import Data
import requests
from tests.conftest import load_json_fixture


class PlenarioResponse:

    def __init__(self, json_payload: dict, session: requests.Session=None, mock: bool=False):
        self.payload: dict = json_payload
        self._meta: Meta = Meta(self.payload.get('meta'))
        self._data: Data = Data(self.payload.get('data'))
        self._session = session
        self._mock = mock  # for testing

    def __iter__(self):
        while self.meta.next_page_link:
            if self._mock is False:
                response = self._session.get(self.meta.next_page_link)
                next_page = PlenarioResponse(response.json(), self._session)
            else:
                # if mocking, json.loads() is used rather than requests
                response = load_json_fixture(self.meta.next_page_link)
                next_page = PlenarioResponse(response)
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
