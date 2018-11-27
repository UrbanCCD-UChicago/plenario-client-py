from plenario_client import PlenarioClient, F
from plenario_client.responses import DataSet, Page


class TestClient:
    """
    These tests are integration tests against the live server.
    """

    def setup_method(self):
        self.client = PlenarioClient(protocol='https', domain='dev.plenar.io')

    def test_list_data_sets(self):
        data_sets = self.client.list_data_sets()
        assert len(data_sets) >= 1

        for meta in data_sets:
            assert isinstance(meta, dict)
            assert 'name' in meta
            assert 'slug' in meta
            assert 'hull' in meta
            assert 'time_range' in meta
            assert 'num_records' in meta

    def test_get_data_set(self):
        data_set = self.client.get_data_set('chicago-311-tree-trims')
        assert isinstance(data_set, DataSet)
        assert isinstance(data_set.page, Page)
        
        i = 0
        for page in data_set:
            assert isinstance(page.meta, dict)
            assert isinstance(page.data, list)
            assert hasattr(page, 'previous_url')
            assert hasattr(page, 'current_url')
            assert hasattr(page, 'next_url')
            assert hasattr(page, 'query')

            i += 1
            if i >= 3:
                break
