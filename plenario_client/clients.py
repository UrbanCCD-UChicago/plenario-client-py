from typing import List

import requests
from requests import Session

from .abc import ClientBase, ResponseHandler
from .filters import F
from .responses import DataSet, Description


class Client(ClientBase):
    """
    A ``Client`` is the access vehicle to the Plenario API. It makes creating requests
    and queries as simple as possible by allowing the user to only provide resource
    identifiers and naturally build queries for filters.
    """

    ENDPOINT = 'data-sets'

    def describe_data_sets(self, params: F=None) -> List[Description]:
        """Sends a request to the ``/data-sets`` list endpoint to get a list of data set
        metadata objects.

        :param params: Query filters (optional).
        :return: A list of data set metadata objects, as :class:`Description`.

        .. example::

        >>> from plenario_client import Client
        >>> client = Client()
        >>> metas = client.describe_data_sets()
        >>> for meta in metas:
        ...     print(meta.name)
        ...     print(meta.slug)
        """
        return self._send_request(url=self.base_path, params=params, parse_as=Description)

    def head_data_set_descriptions(self, params: F=None) -> Description:
        """Sends a request to the ``/data-sets/@head`` list endpoint to get a single data set
        metadata object.

        :param params: Query filters (optional).
        :return: A single data set metadata object, as :class:`Description`.

        .. example::

        >>> from plenario_client import Client
        >>> client = Client()
        >>> meta = client.head_data_set_descriptions()
        >>> print(meta.name)
        >>> print(meta.slug)
        """
        url = f'{self.base_path}/@head'
        return self._send_request(url=url, params=params, parse_as=Description)

    def get_data_set(self, slug: str, params: F=None) -> DataSet:
        """Sends a request to the ``/data-sets/:slug`` detail endpoint to get the records
        of the named data set.

        :param slug: The slug value of the data set.
        :param params: Query filters (optional).
        :return: A list of records wrapped in a :class:`DataSet`

        .. example::

        >>> from plenario_client import Client()
        >>> client = Client()
        >>> data_set = client.get_data_set(slug='chicago-beach-lab-dna-tests')
        >>> for page in data_set:
        ...     do_something_with(page.records)
        """
        url = f'{self.base_path}/{slug}'
        return self._send_request(url=url, params=params, parse_as=DataSet)

    def describe_data_set(self, slug: str, params: F=None) -> Description:
        """Sends a request to the ``/data-sets/:slug/@describe`` detail endpoint to get
        the metadata entry for the data set.

        :param slug: The slug value of the data set.
        :param params: Query filters (optional).
        :return: The metadata entry for the data set, as a :class:`Description`.

        .. example::

        >>> from plenario_client import Client()
        >>> client = Client()
        >>> meta = client.describe_data_set(slug='chicago-beach-lab-dna-tests')
        >>> print(meta.name)
        >>> print(meta.source_url)
        >>> print(meta.latest_import)
        """
        url = f'{self.base_path}/{slug}/@describe'
        return self._send_request(url, params=params, parse_as=Description)

    def head_data_set(self, slug: str, params: F=None) -> DataSet:
        """Sends a request to the ``/data-sets/:slug/@head`` detail endpoint to get a
        seingle record from the data set. Just like :function:`get_data_set` this will
        return the response wrapped as a :class:`DataSet`, but the ``records``
        attribute will only have a single record in its list.

        :param slug: The slug value of the data set.
        :param params: Query filters (optional).
        :return: A single record wrapped in a :class:`DataSet`

        .. example::

        >>> from plenario_client import Client()
        >>> client = Client()
        >>> data_set = client.head_data_set(slug='chicago-beach-lab-dna-tests')
        >>> print(data_set.records[0])
        """
        url = f'{self.base_path}/{slug}/@head'
        return self._send_request(url=url, params=params, parse_as=DataSet)


class AoTClient(ClientBase):
    """
    An ``AoTClient`` is the access vehicle to the Plenario Array of Things API.
    It makes creating requests and queries as simple as possible while allowing the user
    optionally naturally build queries for filters.
    """

    ENDPOINT = 'aot'

    def describe_networks(self, params: F=None) -> List[Description]:
        """Sends a request to the ``/aot/@describe`` endpoint to get a list of network
        metadata objects.

        :param params: Query filters (optional).
        :return: A list of data set metadata objects, as :class:`Description`.

        .. example::

        >>> from plenario_client import AoTClient
        >>> client = AoTClient()
        >>> metas = client.describe_networks()
        >>> for meta in metas:
        ...     print(meta.name)
        ...     print(meta.slug)
        """
        url = f'{self.base_path}/@describe'
        return self._send_request(url=url, params=params, parse_as=Description)

    def get_observations(self, params: F=None) -> DataSet:
        """Sends a request to the ``/aot`` detail endpoint to page through the observations.

        :param params: Query filters (optional).
        :return: A list of records wrapped in a :class:`DataSet`

        .. example::

        >>> from plenario_client import AoTClient()
        >>> client = AoTClient()
        >>> data_set = client.get_observations()
        >>> for page in data_set:
        ...     do_something_with(page.records)
        """
        return self._send_request(url=self.base_path, params=params, parse_as=DataSet)

    def head_observations(self, params: F=None) -> DataSet:
        """Sends a request to the ``/aot/@head`` list endpoint to get a single observation.

        :param params: Query filters (optional).
        :return: A single data set observation, as :class:`DataSet`.

        .. example::

        >>> from plenario_client import AoTClient
        >>> client = AoTClient()
        >>> ds = client.head_observations()
        >>> print(ds.records)
        """
        url = f'{self.base_path}/@head'
        return self._send_request(url=url, params=params, parse_as=DataSet)
