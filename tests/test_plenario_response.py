from tests.test_data_response import DATA
from tests.test_meta_response import PARAMS, LINKS, COUNTS
from tests.conftest import load_json_fixture
from plenario_response.response import PlenarioResponse


json = load_json_fixture()
plenario_response = PlenarioResponse(json)


def test_plenario_response():
    assert plenario_response is not None


def test_plenario_response_meta():
    assert plenario_response.meta.params == PARAMS
    assert plenario_response.meta.links == LINKS
    assert plenario_response.meta.counts == COUNTS


def test_plenario_response_data():
    assert plenario_response.data.dataset == DATA
