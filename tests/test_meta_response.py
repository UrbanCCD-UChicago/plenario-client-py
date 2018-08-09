from tests.conftest import load_json_fixture
from plenario_response.meta import Meta

PARAMS = {
    "page_size": 500,
    "page": 1
}
LINKS = {
    "previous": None,
    "next": "http://localhost:4000/api/v2/data-sets/chicago-beach-lab-data-dna-tests?page_size=500&page=2",
    "current": "http://localhost:4000/api/v2/data-sets/chicago-beach-lab-data-dna-tests?page_size=500&page=1"
}
COUNTS = {
    "total_records": 4381,
    "total_pages": 9,
    "errors": 0,
    "data": 500
}
json = load_json_fixture()
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
