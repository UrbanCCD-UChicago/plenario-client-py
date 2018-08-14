from plenario_client import Client, F

if __name__ == '__main__':
    client = Client(scheme='http', host='localhost:4000', version='v2')
    # client = Client()

    tsrange = '{"lower":"2018-04-01T00:00:00","upper":"2018-09-01T00:00:00","upper_inclusive":false,"lower_inclusive":true}'

    descriptions = client.describe_data_sets(
        params={'time_range': 'intersects:{tsrange}'.format(tsrange=tsrange)})
    for description in descriptions:
        timestamp = [
            field['name']
            for field in description.fields
            if field['type'] == 'timestamp'
        ][0]

        print('Paging through "{name}"'.format(name=description.name))

        data_set = client.get_data_set(
            slug=description.slug, params={timestamp: 'within:{tsrange}'.format(tsrange=tsrange)})
        for page in data_set:
            print('> {page}'.format(page=page))
            print('>> {meta}'.format(meta=page.meta))
            print('>> {size}'.format(size=len(page.records)))

        print('\n')

    from pprint import pprint

    f1 = F()
    f1 &= ('timestamp', 'gt', 'three days ago')
    f1 &= ('location', 'within', 'chicago')

    pprint(f1.to_query_params())

    f2 = F('time_range', 'contains', 'yesterday')
    f1 &= f2

    pprint(f1.to_query_params())

    f1 &= ('node_id', 'eq', '080')
    f1 &= ('node_id', 'eq', '081')

    pprint(f1.to_query_params())

    f1 |= ('timestamp', 'lt', 'today')
    f1 |= F('location', 'outside', 'town')

    pprint(f1.to_query_params())
