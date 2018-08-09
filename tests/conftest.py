import pytest
import json


@pytest.fixture
def load_json_fixture():
    with open("tests/fixtures/chicago_beach_lab_dna_tests_page_one.json") as f:
        return json.load(f)
