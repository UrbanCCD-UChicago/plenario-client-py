import re

import pytest
import responses
from datetime import datetime, date
from plenario_client import Client
from plenario_client.errors import ApiError
from plenario_client.responses import DataSet, Description, PlenarioResponse, TimeRange

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

    assert description.time_range.lower_bound == datetime(2001, 4, 6, 0, 0, 0)
    assert description.time_range.upper_bound == datetime(2018, 8, 13, 0, 0, 1)
    assert description.time_range.lower_inclusive is True
    assert description.time_range.upper_inclusive is False
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


def test_time_range_normalization():
    tr_one = {
        'lower': '2018-01-01T00:00:00',
        'upper': '2018-12-31T23:59:59',
        'lower_inclusive': True,
        'upper_inclusive': True
    }

    tr_two = {
        'lower': '2018-01-01T00:00:00',
        'upper': '2018-12-31T23:59:59',
        'lower_inclusive': False,
        'upper_inclusive': False
    }

    normalized_upper_tr = TimeRange(tr_one)
    normalized_lower_tr = TimeRange(tr_two)

    assert normalized_upper_tr.upper_bound == datetime(2019, 1, 1, 0, 0, 0)
    assert normalized_upper_tr.upper_inclusive is False

    assert normalized_lower_tr.lower_bound == datetime(2018, 1, 1, 0, 0, 1)
    assert normalized_lower_tr.lower_inclusive is True


def test_time_range_operators():
    tr = {
        'lower': '2018-01-01T00:00:00',
        'upper': '2019-01-01T00:00:00',
        'lower_inclusive': True,
        'upper_inclusive': False
    }

    tr_to_be_normalized = {
        'lower': '2018-01-01T00:00:00',
        'upper': '2018-12-31T23:59:59',
        'lower_inclusive': True,
        'upper_inclusive': True
    }

    tr_min = {
        'lower': '2015-01-01T00:00:00',
        'upper': '2016-01-01T00:00:00',
        'lower_inclusive': True,
        'upper_inclusive': False
    }

    time_range = TimeRange(tr)
    time_range_normalized = TimeRange(tr_to_be_normalized)
    time_range_min = TimeRange(tr_min)
    mid_datetime = datetime(2018, 6, 1, 1, 1, 1)

    assert time_range == time_range_normalized
    assert time_range <= time_range_normalized
    assert time_range >= time_range_normalized
    assert time_range != time_range_min
    assert time_range > time_range_min
    assert time_range_min < time_range
    assert mid_datetime in time_range
    assert mid_datetime not in time_range_min
    assert str(time_range) == """{"lower_bound": "2018-01-01 00:00:00", "lower_inclusive": true, "upper_bound": "2019-01-01 00:00:00", "upper_inclusive": false}"""
