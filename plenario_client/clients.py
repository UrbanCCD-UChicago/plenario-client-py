from typing import List

import requests
from requests import Session

from .__version__ import VERSION
from .errors import ApiError
from .filters import F
from .responses import DataSet


class PlenarioClient:
    """The ``PlenarioClient`` class is the primary use of the library. It
    encapsulates the functionality used to call endpoints of the Plenario API
    and wraps is responses in useful, parseable classes.
    """

    def __init__(self, protocol: str='https', domain: str='plenar.io', version: str='v2'):
        """
        Initializes a new instance.

        :param protocol: The connection protocol to the API
        :param domain: The domain name of the API
        :param version: The version string of the API
        """
        self._base_url = f'{protocol}://{domain}/api/{version}/data-sets'

        self._session = Session()
        self._session.headers['User-Agent'] = f'plenario-client-py v{VERSION}'

    def _send_request(self, url: str, params: F=None) -> dict:
        if params:
            params = params.to_query_params()

        resp = self._session.get(url, params=params)
        if resp.status_code != 200:
            raise ApiError(resp.content)

        return resp.json()

    def list_data_sets(self, params: F=None) -> List[dict]:
        """
        Gets a list of data set metadata from the API. The metadata returned
        are the listings of all available data sets. This list can be optionally
        filtered against.

        :param params: An :class:``F`` object used to create query params
        
        :return: The metadata entries for all available data sets
        
        :raise ApiError: Non 200 responses will raise with the message sent

        .. example::

        >>> from plenario_client import PlenarioClient
        >>> client = PlenarioClient()
        >>> data_sets = client.list_data_sets()
        >>> data_sets[0]
        {
            "name": "Chicago 311 - Tree Trims",
            "slug": "chicago-311-tree-trims",
            "hull": { ... },
            "time_range": { ... },
            "num_records": 362192,
            ...
        }
        """
        resp = self._send_request(self._base_url, params)

        data_sets = []
        data = resp.get('data', [])
        while len(data) > 0:
            data_sets.extend(data)
            next_url = resp.get('meta', {}).get('links', {}).get('next_url')
            if not next_url:
                break
            resp = self._send_request(next_url)
            data = resp.get('data', [])

        return data_sets

    def get_data_set(self, slug: str, params: F=None) -> DataSet:
        """
        Gets the records for a given data set from the API. The records can
        be optionally filtered against.

        Since the API returns results in pages, the returned data of this
        response works as a simple iterator wrapper around pages of records.
        See the example below.

        :param slug: The ``slug`` value of the data set
        :param params: An :class:``F`` object used to create query params

        :return: An iterator wrapper for pages of records.

        :raise ApiError: Non 200 responses will raise with the message sent

        .. example::

        >>> from plenario_client import PlenarioClient
        >>> client = PlenarioClient()
        >>> data_set = client.get_data_set('chicago-311-tree-trims')
        >>> for page in data_set:
        ...     print(len(page.data))
        ...     print(page.data[0])
        ... 
        200
        {
            ":id": "row-qre9_vj58_fwye", 
            ":created_at": "2018-11-24T09:17:02", 
            ":updated_at": "2018-11-24T09:17:06", 
            "location": { ... }, 
            "police_district": 9, 
            "service_request_number": "18-01986721", 
            "status": "Completed", 
            "street_address": "2522 S MARY ST", 
            "type_of_service_request": "Tree Trim", 
            "ward": 11, 
            ...
        }
        200
        {
            ":id": "row-vdhr~45ub-am7z", 
            ":created_at": "2018-11-24T09:17:02", 
            ":updated_at": "2018-11-24T09:17:06", 
            "location": { ... }, 
            "police_district": 9, 
            "service_request_number": "18-01986810", 
            "status": "Completed", 
            "street_address": "2505 S MARY ST", 
            "type_of_service_request": "Tree Trim", 
            "ward": 11, 
            ...
        }
        54
        {
            ":id": "row-unfn_ttyb-4fps", 
            ":created_at": "2018-11-24T09:17:02", 
            ":updated_at": "2018-11-24T09:17:06", 
            "location": { ... }, 
            "police_district": 24, 
            "service_request_number": "18-02296466", 
            "status": "Completed", 
            "street_address": "2101 W HOOD AVE", 
            "type_of_service_request": "Tree Trim", 
            "ward": 40, 
            ...
        }
        """
        url = f'{self._base_url}/{slug}'
        resp = self._send_request(url, params)
        return DataSet(self, resp)