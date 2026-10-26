===========
param-store
===========

.. image:: https://img.shields.io/pypi/v/param-store
    :target: https://pypi.org/project/param-store/
    :alt: PyPI

.. image:: https://github.com/labd/python-param-store/actions/workflows/python-test.yml/badge.svg
    :target: https://github.com/labd/python-param-store/actions/workflows/python-test.yml
    :alt: Python Tests

param-store works with parameter stores (e.g. EC2 Parameter Store) to resolve specific parameters.
It is designed to be pluggable so that stores can be created for e.g. Vault or Azure Key Vault.

A use-case is to store secrets in the EC2 parameter store and resolve them automatically.

Installation
============

.. code-block:: shell

   pip install param-store


Usage
=====

As a standalone package

.. code-block:: python

    from param_store import EC2ParameterStore
    from param_store import interpolate_dict

    data = {
        'key': 'my-secret-{{ parameter-1 }}'
    }

    store = EC2ParameterStore()
    result = interpolate_dict(data, store)
    assert result[key] == 'my-secret-password'


In combination with django-environ

.. code-block:: python

    from environ import Env
    from param_store import EC2ParameterStore
    from param_store.contrib import resolve_django_environ

    env = Env()
    store = EC2ParameterStore()
    resolve_django_environ(env, store)
