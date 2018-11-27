from typing import List


class Page:

    def __init__(self, resp: dict):
        self.meta: dict = resp.get('meta', {})
        self.data: List[dict] = resp.get('data', [])

        _links: dict = self.meta.get('links', {})
        self.previous_url: str = _links.get('previous_url')
        self.current_url: str = _links.get('current_url')
        if not len(self.data):
            self.next_url = None
        else:
            self.next_url: str = _links.get('next_url')

        self.query: dict = self.meta.get('query')


class DataSet:

    def __init__(self, client: 'Client', resp: dict):
        self._client = client
        self.page: Page = Page(resp)

    def __iter__(self):
        while self.page.next_url:
            yield self.page

            resp = self._client._send_request(self.page.next_url)
            self.page = Page(resp)

        yield self.page