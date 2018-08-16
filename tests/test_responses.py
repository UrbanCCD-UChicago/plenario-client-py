import re

import pytest
import responses
from datetime import datetime, date
from plenario_client import Client
from plenario_client.errors import ApiError
from plenario_client.responses import DataSet, Description, PlenarioResponse

from utils import load_fixture


PAGE_2_URL = re.compile('.*page=2.*')


def test_response_init_with_error():
    res = load_fixture('error.json')
    with pytest.raises(ApiError):
        PlenarioResponse(res)


def test_response_init_with_list():
    payload = load_fixture('list.json')
    res = PlenarioResponse(payload)

    assert res.meta == payload['meta']
    assert res.data == payload['data']


def test_response_init_with_detail():
    payload = load_fixture('detail.json')
    res = PlenarioResponse(payload)

    assert res.meta == payload['meta']
    assert res.data == payload['data']


def test_description_init():
    payload = load_fixture('list-head.json')
    description = Description(**payload['data'][0])

    assert description.name == 'Chicago 311 Service Requests - Abandoned Vehicles'

    assert description.bbox == {
        'coordinates': [[
            [-87.52468278255836, 41.64449686770894],
            [-87.91372610600482, 41.64449686770894],
            [-87.91372610600482, 42.02266026807753],
            [-87.52468278255836, 42.02266026807753],
            [-87.52468278255836, 41.64449686770894]
        ]],
        'srid': 4326
    }

    assert description.time_range == {
        'lower': '2001-04-06T00:00:00',
        'lower_inclusive': True,
        'upper': '2018-08-13T00:00:00',
        'upper_inclusive': True
    }

    assert description.first_import == datetime(2018, 8, 2, 16, 22)
    assert description.next_import == datetime(2018, 8, 15, 16, 22)
    assert description.latest_import == datetime(2018, 8, 14, 16, 23, 59)
    assert description.refresh_ends_on is None
    assert description.refresh_starts_on == date(2018, 1, 1)



def test_data_set_init():
    payload = load_fixture('detail.json')
    res = PlenarioResponse(payload)
    data_set = DataSet(response=res, client=None)

    assert data_set.meta == res.meta
    assert data_set.records == res.data


@responses.activate
def test_data_set_iter():
    responses.add(
        method=responses.GET,
        url=PAGE_2_URL,
        status=200,
        json=load_fixture('detail-page-2.json')
    )

    payload = load_fixture('detail.json')
    res = PlenarioResponse(payload)
    data_set = DataSet(response=res, client=Client())

    pages = [page for page in data_set]
    assert len(pages) == 2
