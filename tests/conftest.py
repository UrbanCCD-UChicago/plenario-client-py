import pytest
import json

RESPONSE_PAGE_ONE = {
  "meta": {
    "params": {
      "page_size": 500,
      "page": 1
    },
    "links": {
      "previous": None,
      "next": "http://localhost:4000/api/v2/data-sets/chicago-beach-lab-data-dna-tests?page_size=500&page=2",
      "current": "http://localhost:4000/api/v2/data-sets/chicago-beach-lab-data-dna-tests?page_size=500&page=1"
    },
    "counts": {
      "total_records": 4381,
      "total_pages": 9,
      "errors": 0,
      "data": 500
    }
  },
  "data": [
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
}

RESPONSE_PAGE_TWO = {
  "meta": {
    "params": {
      "page_size": 500,
      "page": 2
    },
    "links": {
      "previous": "http://localhost:4000/api/v2/data-sets/chicago-beach-lab-data-dna-tests?page_size=500&page=1",
      "next": None,
      "current": "http://localhost:4000/api/v2/data-sets/chicago-beach-lab-data-dna-tests?page_size=500&page=2"
    },
    "counts": {
      "total_records": 4381,
      "total_pages": 9,
      "errors": 0,
      "data": 500
    }
  },
  "data": [
    {
      "vpf_tNaE6k34OqpOqiUk": {
        "srid": 4326,
        "coordinates": [
          -87.6515,
          41.9785
        ]
      },
      "row_id": 501,
      "Longitude": -87.6515,
      "Location": "(41.9785, -87.6515)",
      "Latitude": 41.9785,
      "DNA Test ID": 5831,
      "DNA Sample Timestamp": "2017-09-01T00:00:00.000000",
      "DNA Sample 2 Reading": 710,
      "DNA Sample 1 Reading": 280,
      "DNA Reading Mean": 445.9,
      "Culture Test ID": None,
      "Culture Sample Interval": None,
      "Culture Sample 2 Timestamp": None,
      "Culture Sample 2 Reading": None,
      "Culture Sample 1 Timestamp": None,
      "Culture Sample 1 Reading": None,
      "Culture Reading Mean": None,
      "Culture Note": None,
      "Beach": "Foster"
    },
    {
      "vpf_tNaE6k34OqpOqiUk": {
        "srid": 4326,
        "coordinates": [
          -87.6385,
          41.9655
        ]
      },
      "row_id": 502,
      "Longitude": -87.6385,
      "Location": "(41.9655, -87.6385)",
      "Latitude": 41.9655,
      "DNA Test ID": 143,
      "DNA Sample Timestamp": "2015-08-06T00:00:00.000000",
      "DNA Sample 2 Reading": 253.9,
      "DNA Sample 1 Reading": 138.4,
      "DNA Reading Mean": 187,
      "Culture Test ID": "94464",
      "Culture Sample Interval": None,
      "Culture Sample 2 Timestamp": None,
      "Culture Sample 2 Reading": "142.0",
      "Culture Sample 1 Timestamp": "08/06/2015 12:00:00 AM",
      "Culture Sample 1 Reading": "222.0",
      "Culture Reading Mean": "177.5",
      "Culture Note": None,
      "Beach": "Montrose"
    },
    {
      "vpf_tNaE6k34OqpOqiUk": {
        "srid": 4326,
        "coordinates": [
          -87.6515,
          41.9785
        ]
      },
      "row_id": 503,
      "Longitude": -87.6515,
      "Location": "(41.9785, -87.6515)",
      "Latitude": 41.9785,
      "DNA Test ID": 5368,
      "DNA Sample Timestamp": "2017-08-22T00:00:00.000000",
      "DNA Sample 2 Reading": 162,
      "DNA Sample 1 Reading": 369,
      "DNA Reading Mean": 244.5,
      "Culture Test ID": None,
      "Culture Sample Interval": None,
      "Culture Sample 2 Timestamp": None,
      "Culture Sample 2 Reading": None,
      "Culture Sample 1 Timestamp": None,
      "Culture Sample 1 Reading": None,
      "Culture Reading Mean": None,
      "Culture Note": None,
      "Beach": "Foster"
    },
    {
      "vpf_tNaE6k34OqpOqiUk": {
        "srid": 4326,
        "coordinates": [
          -87.551,
          41.758
        ]
      }
    }
  ]
}


@pytest.fixture
def load_json_fixture(path: str) -> dict:
    with open(path) as f:
        return json.load(f)