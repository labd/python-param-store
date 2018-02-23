from param_store import interpolate_dict


def resolve_django_environ(env, store):
    """Decrypt the values in the environ.Env object

    :param env: The django-environ object
    :type env: environ.Env
    :param store: The store to use for resolving parameters
    :type store: param_store.stores.BaseStore

    """
    result = interpolate_dict(env.ENVIRON, store)
    env.ENVIRON = result
