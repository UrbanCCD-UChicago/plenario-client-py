import re

import responses  # the responses testing lib, not our responses module
from plenario_client import Client, F

from utils import load_fixture


LOCALHOST_URL = re.compile('.*localhost.*')


class TestClient:
    def setup_method(self, mtd):
        self.client = Client(scheme='http', host='localhost')

    @responses.activate
    def test_describe_data_sets(self):
        responses.add(
            method=responses.GET,
            url=LOCALHOST_URL,
            status=200,
            json=load_fixture('list.json')
        )

        metas = self.client.describe_data_sets()
        assert len(metas) == 15

    @responses.activate
    def test_head_data_set_descriptions(self):
        responses.add(
            method=responses.GET,
            url=LOCALHOST_URL,
            status=200,
            json=load_fixture('list-head.json')
        )

        metas = self.client.head_data_set_descriptions()
        assert len(metas) == 1

    @responses.activate
    def test_get_data_set(self):
        responses.add(
            method=responses.GET,
            url=LOCALHOST_URL,
            status=200,
            json=load_fixture('detail.json')
        )

        data_set = self.client.get_data_set('whatever this is mocked')
        assert data_set.meta == {
            'counts': {
                'data_count': 200,
                'total_pages': 23,
                'total_records': 4520
            },
            'links': {
                'current': 'http://localhost/api/v2/data-sets/chicago-beach-lab-data-dna-tests?order_by=asc%3Arow_id&page=1&page_size=200',
                'next': 'http://localhost/api/v2/data-sets/chicago-beach-lab-data-dna-tests?order_by=asc%3Arow_id&page=2&page_size=200',
                'previous': None
            },
            'params': {
                'order_by': {
                    'asc': 'row_id'
                },
                'page': 1,
                'page_size': 200
            }
        }

    @responses.activate
    def test_describe_data_set(self):
        responses.add(
            method=responses.GET,
            url=LOCALHOST_URL,
            status=200,
            json=load_fixture('detail-describe.json')
        )

        description = self.client.describe_data_set('whatever')
        assert description.name == 'Chicago Beach Lab Data - DNA Tests'

    @responses.activate
    def test_head_data_set(self):
        responses.add(
            method=responses.GET,
            url=LOCALHOST_URL,
            status=200,
            json=load_fixture('detail-head.json')
        )

        data_set = self.client.head_data_set('whatever')
        assert len(data_set.records) == 1

    @responses.activate
    def test_describe_data_sets_with_a_filter(self):
        responses.add(
            method=responses.GET,
            url=LOCALHOST_URL,
            status=200,
            json=load_fixture('list-filtered.json')
        )

        params = F('name', 'eq', 'Chicago Beach Lab Data - DNA Tests')
        params &= ('name', 'eq', 'whatever i do not exist')

        metas = self.client.describe_data_sets(params=params)
        assert len(metas) == 1