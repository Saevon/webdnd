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


class CacheException(Exception):
    pass

class CacheDirty(CacheException):
    def __init__(self, key):
        self.key = key
        super(CacheDirty, self).__init__()

class CacheUnused(CacheException):
    pass


def cache(func):
    '''
    Caches multiple cache results based on a cache_key
    '''
    cache_attr = '_%s__cache' % func.__name__
    cache_key_attr = '_%s_cache_key' % func.__name__
    cache_reset_key = '_reset_cache'

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
        unused = False
        try:
            cache_key = getattr(self, cache_key_attr, lambda *args, **kwargs: '')(*args, **kwargs)
        except CacheDirty as err:
            reset = True
            cache_key = err.key
        except CacheUnused:
            unused = True

        # Find the value
        if unused:
            return func(self, *args, **kwargs)
        elif not reset and cache.get(cache_key):
            return cache.get(cache_key)
        else:
            val = func(self, *args, **kwargs)
            cache[cache_key] = val
            return val

    return wrapper

def dirty_cache(func):
    '''
    Caches the result of the given method, re-running the method only if it is marked as dirty
    '''
    cache_attr = '_%s__cache' % func.__name__
    cache_dirty_attr = '_%s_dirty' % func.__name__
    cache_reset_key = '_reset_cache'

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Check for a cache reset
        reset = kwargs.get(cache_reset_key, False)
        kwargs.pop(cache_reset_key, None)

        reset = reset or getattr(self, cache_dirty_attr, False)
        setattr(self, cache_dirty_attr, False)

        # Reset the cache if needed
        if reset:
            try:
                delattr(self, cache_attr)
            except AttributeError:
                pass

        # Get the cache attributes
        try:
            cache = getattr(self, cache_attr)
        except AttributeError:
            cache = func(self, *args, **kwargs)
            setattr(self, cache_attr, cache)

        return cache

    return wrapper





