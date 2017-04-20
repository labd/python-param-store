from environ import Env

from param_store.contrib import resolve_django_environ

from .utils import MockStore


def test_decrypt_env(monkeypatch):
    monkeypatch.setattr(Env, 'ENVIRON', {
        'TEST_VAR': 'ok',
        'TEST_DECRYPT': 'prefix-%{key-name}-data-%{missing}'
    })

    store = MockStore({
        'key-name': 'secret'
    })

    env = Env()
    resolve_django_environ(env, store)

    assert env.str('TEST_VAR') == 'ok'
    assert env.str('TEST_DECRYPT') == 'prefix-secret-data-%{missing}'
