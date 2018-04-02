import functools
from flask import make_response


def cache_control(directives):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            rv = f(*args, **kwargs)
            rv = make_response(rv)
            rv.headers['Cache-Control'] = ', '.join(directives)
            return rv
        return wrapped
    return decorator
