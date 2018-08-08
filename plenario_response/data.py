class Data:

    def __init__(self, json_payload: dict):
        self._data: dict = json_payload

    @property
    def data(self) -> dict:
        return self._data

    @property
    def count(self) -> int:
        return len(self._data)
