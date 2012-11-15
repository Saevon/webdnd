from django.http import HttpResponse
from functools import wraps
import simplejson


def cascade(func):
    """
    class method decorator, always returns the
    object that called the method
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self
    return wrapper


def json_return(func):
    """
    Wraps the returned object in a HttpResponse after a json dump,
    returning that instead. Unless the return is a HttpResponse
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)

        if isinstance(data, HttpResponse):
            return data

        response = HttpResponse(mimetype='application/json')
        simplejson.dump(data, response)
        return response
    return wrapper


def cache(func):
    cache_attr = '_%s__cache' % func.__name__
    cache_key_attr = '_%s_cache_key' % func.__name__
    cache_reset_key = '_cache_reset'

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Make sure the object has a cache for this value
        if not hasattr(self, cache_attr):
            setattr(self, cache_attr, {})

        # Check for a cache reset
        reset = kwargs.get(cache_reset_key, False)
        kwargs.pop(cache_reset_key, None)

        # Get the cache attributes
        cache = getattr(self, cache_attr)
        cache_key = getattr(self, cache_key_attr, lambda *args, **kwargs: '')(*args, **kwargs)

        # Find the value
        if not reset and cache.get(cache_key):
            print 'cache get'
            return cache.get(cache_key)
        else:
            print 'calc'
            val = func(self, *args, **kwargs)
            cache[cache_key] = val
            return val

    return wrapper


