from plenario_response.meta import Meta


class PlenarioResponse:

    def __init__(self, json_payload: dict):
        self.payload: dict = json_payload
        self.meta: Meta = Meta(self.payload.get('meta'))

    def get_meta(self) -> Meta:
        return self.meta
