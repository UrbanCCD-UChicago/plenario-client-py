from plenario_response.meta import Meta
from plenario_response.data import Data

class PlenarioResponse:

    def __init__(self, json_payload: dict):
        self.payload: dict = json_payload
        self._meta: Meta = Meta(self.payload.get('meta'))
        self._data: Data = Data(self.payload.get('data'))

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def data(self) -> Data:
        return self._data
