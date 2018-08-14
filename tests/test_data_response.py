from tests.conftest import load_json_fixture
from tests.conftest import RESPONSE_PAGE_ONE
from plenario_response.data import Data

DATA_PAGE_ONE = RESPONSE_PAGE_ONE.get('data')
json = load_json_fixture("tests/fixtures/chicago_beach_lab_dna_tests_page_one.json")
data = Data(json.get('data'))


def test_data_response():
    assert data is not None


def test_data_response_dataset():
    assert data.dataset == DATA_PAGE_ONE


def test_data_count():
    assert data.count == len(DATA_PAGE_ONE)
