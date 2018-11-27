# Plenario Client

This library serves as the official Python client to the
[Plenario API](https://plenario.docs.apiary.io/#).

## Requirements

This will run on Python 3.6 or better. Older versions of Python are not
supported. This library requires the installation of the
[requests library](http://docs.python-requests.org/en/master/).

## Usage

There are 2 API endpoints to Plenario:

- The list endpoint that gets metadata about the data sets
- The detail endpoint that gets records from the data sets

### Accessing Data Set Records

Plenario API responses are paginated, so naturally we need to provide users
with the ability to page through data as easily as possible. To do this, we
provide a simple iterator baked into the data sets:

```python
from plenario_client import PlenarioClient

client = PlenarioClient()
data_set = client.get_data_set('chicago-stuff')
for page in data_set:
    do_something_with_the(page)
```

The _page_ here is the response object: it has a `meta` attribute that includes
the response metadata and a `records` attribute that includes the response
body -- a list of dictionaries.

### Filtering with Query Parameters

Filtering can be a little complicated depending on your needs. To handle that,
we've come up with a pretty simple solution. Somewhat similar to Django and
Elasticsearch-DSL we have an `F` class with which you construct and compose
query parameters to filter the results.

There are three operations:

- Basic init with `F('field name', 'query operator', 'query value')`
- Appending filters with `F() &= F()`
- Overriding filters with `F() |= F()`

Here's an example:

```python
from plenario_client import PlenarioClient, F

# let's build a filter where we want items whose name is 'vince'
# and their age is greater than or equal to 21:
params = F('name', 'eq', 'vince')
params &= ('age', 'ge', 21)  # appending works with either an F or a tuple

# let's now say we want to add 'bob' to the filter as well:
params &= ('name', 'eq', 'bob')

# at this point if we inspect the filter we would get something like
{
    'name': [
        ('eq', 'vince'),
        ('eq', 'bob')
    ],
    'age': ('ge', 21)
}

# now let's say that due to some logic happening in our script,
# we've determined that neither 'vince' nor 'bob' are desireable
# values -- we need 'alice':
params |= ('name', 'eq', 'alice')

# now under the hood, our filter looks like
{
    'name': ('eq', 'alice'),
    'age': ('ge', 21)
}

# now we're ready to fire off the request:
client = PlenarioClient()
client.describe_data_sets(params=params)
```

## Developing and Contributing

To run the tests locally:

```bash
$ pipenv install --dev
$ pipenv run python -m pytest
```

To push a relase to PyPI:

```bash
$ pipenv run python setup.py sdist bdist_wheel
$ pipenv run twine upload dist/*
```