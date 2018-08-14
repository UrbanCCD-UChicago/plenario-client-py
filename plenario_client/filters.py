from typing import Dict, List, Tuple


class F:

    def __init__(self, *args):
        self.filters: Dict[str, tuple] = {}

        if args:
            key, op, value = args
            self.filters[key] = (op, value)

    def __iand__(self, other):
        if isinstance(other, F):
            for key, op_value in other.filters.items():
                if key in self.filters:
                    curr_val = self.filters[key]
                    if not isinstance(curr_val, list):
                        curr_val = [curr_val]

                    if isinstance(op_value, list):
                        curr_val.extend(op_value)
                    else:
                        curr_val.append(op_value)
                    self.filters[key] = curr_val

                else:
                    self.filters[key] = op_value

        elif isinstance(other, tuple):
            key, op, value = other

            if key in self.filters:
                curr_val = self.filters[key]
                if not isinstance(curr_val, list):
                    curr_val = [curr_val]
                curr_val.append((op, value))
                self.filters[key] = curr_val

            else:
                self.filters[key] = (op, value)

        else:
            raise TypeError('other is neither F not Tuple')

        return self

    def __ior__(self, other):
        if isinstance(other, F):
            for key, op_value in other.filters.items():
                self.filters[key] = op_value

        elif isinstance(other, tuple):
            key, op, value = other
            self.filters[key] = (op, value)

        else:
            raise TypeError('other is neither F nor Tuple')

        return self

    def to_query_params(self) -> List[Tuple[str, str]]:
        params = []

        for key, op_value in self.filters.items():
            if isinstance(op_value, list):
                key = '{key}[]'.format(key=key)
                for (op, value) in op_value:
                    params.append(
                        (key, '{op}:{value}'.format(op=op, value=value)))
            else:
                op, value = op_value
                params.append((key, '{op}:{value}'.format(op=op, value=value)))

        return params
