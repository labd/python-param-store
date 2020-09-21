import copy
import re

import six

_re_param_template = re.compile(r"({{ \s* ([^(?:}})]+) \s* }})", re.VERBOSE)

__all__ = ["interpolate_dict", "MissingParameterException"]


class MissingParameterException(Exception):
    pass


def interpolate_dict(raw_values, store):
    """Interpolate dictionary values

    DATABASE_URL=postgresql:://user::{{ dbpassword }}/127.0.0.1/db

    :param raw_values: The values to resolv
    :type raw_values: The
    :param store: The store to use for resolving parameters
    :type store: param_store.stores.BaseStore

    :rtype: dict

    """
    parameters_per_key = {}
    required_parameters = []

    # Find parameters to retrieve from the store (new style)
    for key, value in raw_values.items():
        if isinstance(value, six.string_types):
            matches = _re_param_template.findall(value)
            variables = {k: v.strip() for k, v in matches}

            parameters_per_key[key] = variables
            required_parameters.extend(variables.values())

    # Load the data
    resolved_parameters = store.load_values(required_parameters)

    result = copy.deepcopy(raw_values)

    # Update the values with the retrieved parameter values
    for key, key_params in parameters_per_key.items():
        value_str = result[key]
        for variable, identifier in key_params.items():
            try:
                identifier_value = resolved_parameters[identifier]
                value_str = value_str.replace(variable, identifier_value)
            except KeyError:
                raise MissingParameterException(
                    "No parameter for identifier %r in %r"
                    % (identifier, raw_values[key])
                )

        result[key] = value_str
    return result
