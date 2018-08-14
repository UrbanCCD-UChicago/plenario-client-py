from typing import List

import requests
from requests import Session

from .errors import ApiError
from .responses import DataSet, Description, Response


class Client:
    """A ``Client`` is the access vehicle to the Plenario API. It makes creating requests
    and queries as simple as possible by allowing the user to only provide resource
    identifiers and naturally build queries for filters.
    """

    def __init__(self, scheme: str='https', host: str='dev.plenar.io', version: str='v2'):
        """Initializes a new ``Client``.

        :param scheme: Either ``http`` or ``https``. Defaults to ``https``.
        :param host: The hostname of the API. Defaults to ``dev.plenar.io``.
        :param version: The version number of the API. Defaults to ``v2``.

        .. example::
        >>> # say we want to test against a local dev version of the API
        >>> from plenario_client import Client
        >>> client = Client(scheme='http', host='localhost:4000', version='x2.1')
        """
        self.scheme: str = scheme
        self.host: str = host
        self.version: str = version

        self.base_path = '{scheme}://{host}/api/{version}/data-sets'.format(
            scheme=self.scheme, host=self.host, version=self.version)

        self.session = Session()

    def describe_data_sets(self, params: dict=None) -> List[Description]:
        """Sends a request to the ``/data-sets`` list endpoint to get a list of data set
        metadata objects.

        :param params: A dictionary of query parameters (optional).
        :return: A list of data set metadata objects, as :class:`Description`.

        .. example::

        >>> from plenario_client import Client
        >>> client = Client()
        >>> metas = client.describe_data_sets()
        >>> for meta in metas:
        ...     print(meta.name)
        ...     print(meta.slug)
        """
        return self._send_request(self.base_path, params=params, parse_res_as_description=True)

    def head_data_set_descriptions(self, params: dict=None) -> Description:
        """Sends a request to the ``/data-sets/@head`` list endpoint to get a single data set
        metadata object.

        :param params: A dictionary of query parameters (optional).
        :return: A single data set metadata object, as :class:`Description`.

        .. example::

        >>> from plenario_client import Client
        >>> client = Client()
        >>> meta = client.head_data_set_descriptions()
        >>> print(meta.name)
        >>> print(meta.slug)
        """
        url = '{base}/@head'.format(
            base=self.base_path, parse_res_as_description=True)
        return self._send_request(url, params=params, parse_res_as_description=True)

    def get_data_set(self, slug: str, params: dict=None) -> DataSet:
        """Sends a request to the ``/data-sets/:slug`` detail endpoint to get the records
        of the named data set.

        :param slug: The slug value of the data set.
        :param params: A dictionary of query parameters (optional).
        :return: A list of records wrapped in a :class:`DataSet`

        .. example::

        >>> from plenario_client import Client()
        >>> client = Client()
        >>> data_set = client.get_data_set(slug='chicago-beach-lab-dna-tests')
        >>> for page in data_set:
        ...     do_something_with(page.records)
        """
        url = '{base}/{slug}'.format(base=self.base_path, slug=slug)
        return self._send_request(url, params=params)

    def describe_data_set(self, slug: str, params: dict=None) -> Description:
        """Sends a request to the ``/data-sets/:slug/@describe`` detail endpoint to get
        the metadata entry for the data set.

        :param slug: The slug value of the data set.
        :param params: A dictionary of query parameters (optional).
        :return: The metadata entry for the data set, as a :class:`Description`.

        .. example::

        >>> from plenario_client import Client()
        >>> client = Client()
        >>> meta = client.describe_data_set(slug='chicago-beach-lab-dna-tests')
        >>> print(meta.name)
        >>> print(meta.source_url)
        >>> print(meta.latest_import)
        """
        url = '{base}/{slug}/@describe'.format(base=self.base_path, slug=slug)
        return self._send_request(url, params=params, parse_res_as_description=True)

    def head_data_set(self, slug: str, params: dict=None) -> DataSet:
        """Sends a request to the ``/data-sets/:slug/@head`` detail endpoint to get a
        seingle record from the data set. Just like :function:`get_data_set` this will
        return the response wrapped as a :class:`DataSet`, but the ``records``
        attribute will only have a single record in its list.

        :param slug: The slug value of the data set.
        :param params: A dictionary of query parameters (optional).
        :return: A single record wrapped in a :class:`DataSet`

        .. example::

        >>> from plenario_client import Client()
        >>> client = Client()
        >>> data_set = client.head_data_set(slug='chicago-beach-lab-dna-tests')
        >>> print(data_set.records[0])
        """
        url = '{base}/{slug}/@head'.format(base=self.base_path, slug=slug)
        return self._send_request(url, params=params)

    def _send_request(self, url: str, params: dict=None, parse_res_as_description: bool=False) -> Response:
        # sends the actual request, handles the response, and parses the response
        # body into the appropriate type. requests are assumed to be to the detail
        # endpoint, but requests made to metadata endpoints must specify the
        # `parse_res_as_description` flag as `True`.
        res = self.session.get(url, params=params)
        payload = res.json()

        if 'error' in payload:
            raise ApiError(payload['error'])

        if parse_res_as_description:
            return [Description(**meta) for meta in payload.get('data')]
        else:
            response = Response(payload)
            return DataSet(response=response, client=self)
