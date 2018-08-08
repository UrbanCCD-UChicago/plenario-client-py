import pytest
import json
from plenario_response.meta import Meta

PARAMS = {
    "page_size": 500,
    "page": 1
}
COUNTS = {
    "total_records": 4381,
    "total_pages": 9,
    "errors": 0,
    "data": 500
}
LINKS = {
    "previous": None,
    "next": "http://localhost:4000/api/v2/data-sets/chicago-beach-lab-data-dna-tests?page_size=500&page=2",
    "current": "http://localhost:4000/api/v2/data-sets/chicago-beach-lab-data-dna-tests?page_size=500&page=1"
}


@pytest.fixture
def load_json():
    with open("tests/fixtures/chicago_beach_lab_dna_tests_page_one.json") as f:
        return json.load(f)


def test_meta_response():
    meta = Meta(load_json())
    assert meta.page == PARAMS.get("page")
    assert meta.page_size == PARAMS.get("page_size")
    assert meta.counts == COUNTS
    assert meta.current_page_link == LINKS.get("current")
    assert meta.previous_link == LINKS.get("previous")
    assert meta.next_page_link == LINKS.get("next")
