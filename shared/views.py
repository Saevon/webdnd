from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

from functools import wraps
from shared.utils.decorators import json_return

class LoginRequiredMixin(object):
    """
    Ensures that user must be authenticated in order to access view.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ApiError(BaseException):
    pass

class Api(LoginRequiredMixin, View):
    @classmethod
    def as_view(cls, *args, **kwargs):
        out = super(Api, cls).as_view(*args, **kwargs)
        return json_return(Api.api_format(out))

    @staticmethod
    def api_format(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            errors = []
            paging = {}
            try:
                data = func(*args, **kwargs)
            except ApiError as err:
                errors = [err]

            if isinstance(data, list):
                paging = {
                    'page': 1,
                    'pagelen': -1,
                    'pages': 1,
                    'total': len(data)
                }

            return {
                'output': data,
                'errors': errors,
                'paging': paging
            }
        return wrapper

class MixinType(type):
    def __new__(cls, name, bases, dct):
        ret = type.__new__(cls, name, bases, dct)

        if name != 'ModelMixin':
            assert 'model' in dct
            model = dct.pop('model')

            for k, v in dct.iteritems():
                if k not in ModelMixin.__dict__:
                    model.add_to_class(k, v)

        return ret


class ModelMixin(object):
    """
    A Mixin that allows you to update existing django models
    """
    __metaclass__ = MixinType
