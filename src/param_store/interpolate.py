import copy
import re

import six


_re_param_template = re.compile('%{([^}]+)}')

__all__ = [
    'interpolate_dict',
]


def interpolate_dict(raw_values, store):
    """Interpolate dictionary values

    DATABASE_URL=postgresql:://user::%{dbpassword}/127.0.0.1/db

    :param raw_values: The values to resolv
    :type raw_values: The
    :param store: The store to use for resolving parameters
    :type store: param_store.stores.BaseStore

    :rtype: dict

    """
    parameters_per_key = {}
    required_parameters = []

    # Find parameters to retrieve from the store
    for key, value in raw_values.items():
        if isinstance(value, six.string_types):
            matches = _re_param_template.findall(value)
            parameters_per_key[key] = matches
            required_parameters.extend(matches)

    # Load the data
    resolved_parameters = store.load_values(required_parameters)

    result = copy.deepcopy(raw_values)

    # Update the values with the retrieved parameter values
    for key, key_params  in parameters_per_key.items():
        value_str = result[key]
        for param in key_params:
            if param in resolved_parameters:
                value_str = value_str.replace(
                    '%{{{}}}'.format(param), resolved_parameters[param])
        result[key] = value_str

    return result
