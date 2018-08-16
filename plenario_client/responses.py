from datetime import datetime
from typing import List

from .abc import ResponseHandler
from .errors import ApiError


class PlenarioResponse:
    """
    ``Response`` is a generic wrapper around responses from the API. It captures
    the major blocks of the response body -- ``meta`` and ``data`` -- and parses them
    into usable components.
    """

    def __init__(self, response: dict):
        """Initializes a new ``Client``.

        :param response: The JSON body of the API response
        :raise ApiError: When the response payload contains an ``error`` key, the error message
            is raised as the Python error message.
        """
        error = response.get('error')
        if error is not None:
            raise ApiError(error)

        self.meta = response.get('meta', {})
        self.data = response.get('data', {})

        links = self.meta.get('links', {})
        self.previous_url = links.get('previous')
        self.current_url = links.get('current')
        self.next_url = links.get('next')

        counts = self.meta.get('counts', {})
        self.data_count = counts.get('data_count')
        self.total_pages = counts.get('total_pages')
        self.total_records = counts.get('total_records')

        self.params = self.meta.get('params', {})

    def __str__(self) -> str:
        return self.current_url

    def __repr__(self) -> str:
        return '<Response {url}>'.format(url=self.current_url)


class Description(ResponseHandler):
    """
    A ``Description`` is a specific kind of response from the API. There are
    several endpoints of the API that return metadata of the data sets -- this
    object captures those metadata values.

    The metadata of a dataset can be used to create resource requests to access
    the data set records, or to determine fields and filtering possibilities, or
    view significant timestamps, etc.
    """

    def __init__(self, **kwargs):
        """Initializes a new ``Desctiprion``.

        :param attribution: The data set's attribution
        :param bbox: The data set's bounding box
        :param description: The data set's description
        :param fields: The data set's fields
        :param first_import: The data set's first import timestamp
        :param latest_import: The data set's latest import timestamp
        :param name: The data set's name
        :param next_import: The data set's next import timestamp
        :param refresh_ends_on: The data set's refresh ends on timestamp
        :param refresh_interval: The data set's refresh interval
        :param refresh_rate: The data set's refresh rate
        :param refresh_starts_on: The data set's refresh starts on timestamp
        :param slug: The data set's slug
        :param source_url: The data set's source url
        :param time_range: The data set's time range
        :param user: The data set's user
        :param virtual_dates: The data set's virtual dates
        :param virtual_points: The data set's virtual points
        """
        self.attribution: str = kwargs.get('attribution')
        self.bbox: dict = kwargs.get('bbox')
        self.description: str = kwargs.get('description')
        self.fields: List[dict] = kwargs.get('fields')
        self.first_import: datetime = kwargs.get('first_import')
        self.latest_import: datetime = kwargs.get('latest_import')
        self.name: str = kwargs.get('name')
        self.next_import: datetime = kwargs.get('next_import')
        self.refresh_ends_on: datetime = kwargs.get('refresh_ends_on')
        self.refresh_interval: int = kwargs.get('refresh_interval')
        self.refresh_rate: str = kwargs.get('refresh_rate')
        self.refresh_starts_on: datetime = kwargs.get('refresh_starts_on')
        self.slug: str = kwargs.get('slug')
        self.source_url: str = kwargs.get('source_url')
        self.time_range: dict = kwargs.get('time_range')
        self.user: dict = kwargs.get('user')
        self.virtual_dates: List[dict] = kwargs.get('virtual_dates')
        self.virtual_points: List[dict] = kwargs.get('virtual_points')

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<Description name="{name}" slug="{slug}">'.format(name=self.name, slug=self.slug)

    @classmethod
    def from_api_payload(cls, payload: dict, client: 'Client'=None) -> 'Description':
        data = payload.get('data')
        if isinstance(data, list):
            return [cls(**meta) for meta in data]
        else:
            return cls(**data)


class DataSet(ResponseHandler):
    """
    A ``DataSet`` is a thin wrapper around an API resource response. It holds the
    parsed list of records for the request.

    Its most useful feature is its generator ability -- API responses are paginated and
    part of the response metadata are links to successive pages of records. Rather than
    having users manually introspect for a potential next page, the ``DataSet`` wrapper
    allows users to naturally write iterators around paging.

    .. example::

    >>> from plenario_client import Client
    >>> client = Client()
    >>> data_set = client.get_data_set('Chicago Beach Lab - DNA Tests')
    >>> for page in data_set:
    ...     print(page.meta)
    ...
    """

    def __init__(self, client: 'Client', response: PlenarioResponse):
        """Initializes a new ``DataSet``.

        :param client: The :class:`Client` that made the request, got the
            :class:`PlenarioResponse`, and parsed the reponse into this ``DataSet``.
            It's used to make subsequent paging requests to the resource.
        :param response: The :class:`Response` object that will be parsed into this object
        """
        self._client = client
        self._response = response

    def __str__(self) -> str:
        return self._response.current_url

    def __repr__(self) -> str:
        return '<DataSet {self}>'.format(self=self)

    def __iter__(self) -> 'DataSet':
        while self._response.next_url is not None:
            yield self

            refreshed = self._client._send_request(
                url=self._response.next_url, parse_as=DataSet)
            self = refreshed

        yield self

    @classmethod
    def from_api_payload(cls, payload: dict, client: 'Client') -> 'DataSet':
        response = PlenarioResponse(payload)
        return cls(response=response, client=client)

    @property
    def records(self) -> List[dict]:
        """Accessess the underlying :class:`Response` list of records.
        """
        return self._response.data

    @property
    def meta(self) -> dict:
        """Accessess the underlying :class:`Response` metadata.
        """
        return self._response.meta
