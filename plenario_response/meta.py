class Meta:

    def __init__(self, json_payload: dict):
        self.payload = json_payload
        self._params: dict = self.payload.get('params')
        self._links: dict = self.payload.get('links')
        self._counts: dict = self.payload.get('counts')

    @property
    def page(self) -> int:
        return self._params.get('page')

    @property
    def page_size(self) -> int:
        return self._params.get('page_size')

    @property
    def current_page_link(self) -> str:
        return self._links.get('current')

    @property
    def next_page_link(self) -> str:
        return self._links.get('next')

    @property
    def previous_link(self) -> str:
        return self._links.get('previous')

    @property
    def params(self) -> dict:
        return self._params

    @property
    def counts(self) -> dict:
        return self._counts

    @property
    def links(self) -> dict:
        return self._links

