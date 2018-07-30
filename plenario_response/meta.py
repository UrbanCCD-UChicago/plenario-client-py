class Meta:

    def __init__(self, json_payload: dict):
        self.payload: dict = json_payload
        self.params: dict = self.payload.get('params')
        self.links: dict = self.payload.get('links')
        self.counts: dict = self.payload.get('counts')

    @property
    def get_page(self) -> int:
        return self.params.get('page')

    @property
    def get_page_size(self) -> int:
        return self.params.get('page_size')

    @property
    def get_current_page_link(self) -> str:
        return self.links.get('current')

    @property
    def get_next_page_link(self) -> str:
        return self.links.get('next')

    @property
    def get_previous_link(self) -> str:
        return self.links.get('previous')

    @property
    def get_params(self) -> dict:
        return self.params

    @property
    def get_counts(self) -> dict:
        return self.counts
