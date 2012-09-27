from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    Ensures that user must be authenticated in order to access view.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

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