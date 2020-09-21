import pytest
from environ import Env

from param_store import MissingParameterException
from param_store.contrib import resolve_django_environ

from .utils import MockStore


def test_decrypt_env(monkeypatch):
    monkeypatch.setattr(
        Env, "ENVIRON", {"TEST_VAR": "ok", "TEST_DECRYPT": "prefix-{{ key-name }}-data"}
    )

    store = MockStore({"key-name": "secret"})

    env = Env()
    resolve_django_environ(env, store)

    assert env.str("TEST_VAR") == "ok"
    assert env.str("TEST_DECRYPT") == "prefix-secret-data"


def test_decrypt_env_missing_param(monkeypatch):
    monkeypatch.setattr(
        Env,
        "ENVIRON",
        {"TEST_VAR": "ok", "TEST_DECRYPT": "prefix-{{ SECRET_KEY }}-data"},
    )

    store = MockStore({})

    env = Env()

    with pytest.raises(MissingParameterException):
        resolve_django_environ(env, store)
