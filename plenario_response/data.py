class Data:

    def __init__(self, json_payload: dict):
        self._dataset: dict = json_payload

    @property
    def dataset(self) -> dict:
        return self._dataset

    @property
    def count(self) -> int:
        return len(self._dataset)
