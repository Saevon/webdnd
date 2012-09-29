from functools import wraps


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


from django.http import HttpResponse

from functools import wraps
import simplejson


def json_return(func):
    """
    Wraps the returned object in a HttpResponse after a json dump,
    returning that instead
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)

        response = HttpResponse(mimetype='application/json')
        simplejson.dump(data, response)
        return response
    return wrapper
