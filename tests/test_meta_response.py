import pytest
import json
from plenario_response.meta import Meta

PAGE = 1
PAGE_SIZE = 500
COUNTS = {
    "total_records": 4290,
    "total_pages": 9,
    "errors": 0,
    "data": 500
}
LINKS = {
    "previous": None,
    "next": "http://localhost:4000/api/v2/data-sets/chicago-beach-lab-dna-tests?inserted_at=le%3A2018-08-02T18%3A39%3A13.368679&page_size=500&page=2",
    "current": "http://localhost:4000/api/v2/data-sets/chicago-beach-lab-dna-tests?inserted_at=le%3A2018-08-02T18%3A39%3A13.368679&page_size=500&page=1"
}


@pytest.fixture
def load_json():
    with open("fixtures/chicago_beach_lab_dna_tests") as f:
        return json.load(f)


def test_meta_response():
    meta = Meta(load_json())
    assert meta.page == PAGE
    assert meta.page_size == PAGE_SIZE
    assert meta.counts == COUNTS
    assert meta.current_page_link == LINKS.get("current")
    assert meta.previous_link == LINKS.get("previous")
    assert meta.next_page_link == LINKS.get("next")
