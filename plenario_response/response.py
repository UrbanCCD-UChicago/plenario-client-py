from plenario_response.meta import Meta


class PlenarioResponse:

    def __init__(self, json_payload_dict):
        self.payload = json_payload_dict
        self.meta = Meta(self.payload.get('meta'))
