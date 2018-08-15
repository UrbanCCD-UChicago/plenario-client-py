from tests.conftest import load_json_fixture
from tests.conftest import RESPONSE_PAGE_ONE
from plenario_response.meta import Meta

PARAMS = RESPONSE_PAGE_ONE.get('meta').get('params')
LINKS = RESPONSE_PAGE_ONE.get('meta').get('links')
COUNTS = RESPONSE_PAGE_ONE.get('meta').get('counts')
json = load_json_fixture("tests/fixtures/chicago_beach_lab_dna_tests_page_one.json")
meta = Meta(json.get('meta'))


def test_meta_response():
    assert meta is not None


def test_meta_get_page():
    assert meta.page == PARAMS.get("page")


def test_meta_get_page_size():
    assert meta.page_size == PARAMS.get("page_size")


def test_meta_get_counts():
    assert meta.counts == COUNTS


def test_meta_get_current_page():
    assert meta.current_page_link == LINKS.get("current")


def test_meta_get_previous_link():
    assert meta.previous_link == LINKS.get("previous")


def test_meta_get_next_page():
    assert meta.next_page_link == LINKS.get("next")
