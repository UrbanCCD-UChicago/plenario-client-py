from plenario_client import F
from plenario_client.responses import TimeRange


def test_empty_init():
    f = F()
    assert f.filters == {}


def test_tuple_init():
    f = F('age', 'gt', 21)
    assert f.filters == {
        'age': ('gt', 21)
    }


def test_iand_with_a_tuple():
    f = F()
    assert f.filters == {}

    f &= ('name', 'eq', 'vince')
    assert f.filters == {
        'name': ('eq', 'vince')
    }

    f &= ('age', 'gt', 21)
    assert f.filters == {
        'name': ('eq', 'vince'),
        'age': ('gt', 21)
    }

    f &= ('name', 'eq', 'bob')
    assert f.filters == {
        'name': [
            ('eq', 'vince'),
            ('eq', 'bob')
        ],
        'age': ('gt', 21)
    }


def test_iand_with_another_filter():
    f = F()
    assert f.filters == {}

    f &= F('name', 'eq', 'vince')
    assert f.filters == {
        'name': ('eq', 'vince')
    }

    f &= F('age', 'gt', 21)
    assert f.filters == {
        'name': ('eq', 'vince'),
        'age': ('gt', 21)
    }

    f &= F('name', 'eq', 'bob')
    assert f.filters == {
        'name': [
            ('eq', 'vince'),
            ('eq', 'bob')
        ],
        'age': ('gt', 21)
    }


def test_ior_with_a_tuple():
    f = F()
    assert f.filters == {}

    f |= ('name', 'eq', 'vince')
    assert f.filters == {
        'name': ('eq', 'vince')
    }

    f |= ('age', 'gt', 21)
    assert f.filters == {
        'name': ('eq', 'vince'),
        'age': ('gt', 21)
    }

    f |= ('name', 'eq', 'bob')
    assert f.filters == {
        'name': ('eq', 'bob'),
        'age': ('gt', 21)
    }


def test_ior_with_another_filter():
    f = F()
    assert f.filters == {}

    f |= F('name', 'eq', 'vince')
    assert f.filters == {
        'name': ('eq', 'vince')
    }

    f |= F('age', 'gt', 21)
    assert f.filters == {
        'name': ('eq', 'vince'),
        'age': ('gt', 21)
    }

    f |= F('name', 'eq', 'bob')
    assert f.filters == {
        'name': ('eq', 'bob'),
        'age': ('gt', 21)
    }


def test_to_query_params():
    f = F('name', 'eq', 'vince')
    assert f.to_query_params() == [
        ('name', 'eq:vince')
    ]

    f &= ('name', 'eq', 'bob')
    assert f.to_query_params() == [
        ('name[]', 'eq:vince'),
        ('name[]', 'eq:bob')
    ]


def test_time_range_filter():
    tr = {
        'lower': '2018-01-01T00:00:00',
        'upper': '2019-01-01T00:00:00',
        'lower_inclusive': True,
        'upper_inclusive': False
    }

    time_range = TimeRange(tr)
    f = F("timestamp", "within", time_range)
    assert f.to_query_params() == [('timestamp', 'within:{"lower": "2018-01-01T00:00:00", "lower_inclusive": true, "upper": "2019-01-01T00:00:00", "upper_inclusive": false}')]
