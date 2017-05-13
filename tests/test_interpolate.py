from environ import Env

import param_store

from .utils import MockStore


def test_interpolate_dict():
    my_dict = {
        'TEST_VAR': 'ok',
        'TEST_DECRYPT': 'prefix-%{key-name}-data-%{missing}',
        'TEST_DOT': '%{key.name}',
    }

    store = MockStore({
        'key-name': 'secret',
        'key.name': 'geheim'
    })
    result = param_store.interpolate_dict(my_dict, store)

    assert result == {
        'TEST_VAR': 'ok',
        'TEST_DECRYPT': 'prefix-secret-data-%{missing}',
        'TEST_DOT': 'geheim',
    }

