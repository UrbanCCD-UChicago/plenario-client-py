from tests.test_data_response import DATA_PAGE_ONE
from tests.test_meta_response import PARAMS, LINKS, COUNTS
from tests.conftest import load_json_fixture
from tests.conftest import RESPONSE_PAGE_ONE, RESPONSE_PAGE_TWO
from plenario_response.response import PlenarioResponse


json_page_one = load_json_fixture("tests/fixtures/chicago_beach_lab_dna_tests_page_one.json")
plenario_response = PlenarioResponse(json_page_one)


def test_plenario_response():
    assert plenario_response is not None


def test_plenario_response_meta():
    assert plenario_response.meta.params == PARAMS
    assert plenario_response.meta.links == LINKS
    assert plenario_response.meta.counts == COUNTS


def test_plenario_response_data():
    assert plenario_response.data.dataset == DATA_PAGE_ONE


def test_plenario_response_pagination_iterator():
    mock_plenario_response = PlenarioResponse(json_page_one, mock=True)

    # redefine next page link to local json fixture
    mock_plenario_response.meta.next_page_link = "tests/fixtures/chicago_beach_lab_dna_tests_page_two.json"
    RESPONSE_PAGE_ONE['meta']['links']['next'] = "tests/fixtures/chicago_beach_lab_dna_tests_page_two.json"

    pages = []
    for page in mock_plenario_response:
        pages.append(page.payload)

    assert pages == [RESPONSE_PAGE_ONE, RESPONSE_PAGE_TWO]

