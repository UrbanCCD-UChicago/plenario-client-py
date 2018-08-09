from tests.conftest import load_json_fixture
from plenario_response.data import Data

DATA = [
    {
      "vpf_tNaE6k34OqpOqiUk": {
        "srid": 4326,
        "coordinates": [
          -87.6385,
          41.9655
        ]
      },
      "row_id": 1,
      "Longitude": -87.6385,
      "Location": "(41.9655, -87.6385)",
      "Latitude": 41.9655,
      "DNA Test ID": 1606,
      "DNA Sample Timestamp": "2016-08-05T12:35:00.000000",
      "DNA Sample 2 Reading": 163,
      "DNA Sample 1 Reading": 39,
      "DNA Reading Mean": 79.7,
      "Culture Test ID": "113691",
      "Culture Sample Interval": "1",
      "Culture Sample 2 Timestamp": "08/05/2016 08:36:00 AM",
      "Culture Sample 2 Reading": "1733.0",
      "Culture Sample 1 Timestamp": "08/05/2016 08:35:00 AM",
      "Culture Sample 1 Reading": "411.0",
      "Culture Reading Mean": "844.0",
      "Culture Note": None,
      "Beach": "Montrose"
    },
    {
      "vpf_tNaE6k34OqpOqiUk": {
        "srid": 4326,
        "coordinates": [
          -87.5299,
          41.7142
        ]
      },
      "row_id": 2,
      "Longitude": -87.5299,
      "Location": "(41.7142, -87.5299)",
      "Latitude": 41.7142,
      "DNA Test ID": 4585,
      "DNA Sample Timestamp": "2017-07-30T00:00:00.000000",
      "DNA Sample 2 Reading": 389,
      "DNA Sample 1 Reading": 313,
      "DNA Reading Mean": 348.9,
      "Culture Test ID": None,
      "Culture Sample Interval": None,
      "Culture Sample 2 Timestamp": None,
      "Culture Sample 2 Reading": None,
      "Culture Sample 1 Timestamp": None,
      "Culture Sample 1 Reading": None,
      "Culture Reading Mean": None,
      "Culture Note": None,
      "Beach": "Calumet"
    },
    {
      "vpf_tNaE6k34OqpOqiUk": {
        "srid": 4326,
        "coordinates": [
          -87.6545,
          41.9877
        ]
      },
      "row_id": 3,
      "Longitude": -87.6545,
      "Location": "(41.9877, -87.6545)",
      "Latitude": 41.9877,
      "DNA Test ID": 5451,
      "DNA Sample Timestamp": "2017-08-23T00:00:00.000000",
      "DNA Sample 2 Reading": 247,
      "DNA Sample 1 Reading": 87,
      "DNA Reading Mean": 146.6,
      "Culture Test ID": None,
      "Culture Sample Interval": None,
      "Culture Sample 2 Timestamp": None,
      "Culture Sample 2 Reading": None,
      "Culture Sample 1 Timestamp": None,
      "Culture Sample 1 Reading": None,
      "Culture Reading Mean": None,
      "Culture Note": None,
      "Beach": "Osterman"
    }
]
json = load_json_fixture()
data = Data(json.get('data'))


def test_data_response():
    assert data.dataset == DATA


def test_data_count():
    assert data.count == len(DATA)
