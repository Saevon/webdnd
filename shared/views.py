from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

from webdnd.shared.utils.decorators import json_return
from webdnd.shared.utils.api import api_output, http_auth_login
from webdnd.shared.utils.api import InvalidKey

from webdnd.player.models.campaigns import Game

class LoginRequiredMixin(object):
    """
    Ensures that user must be authenticated in order to access view.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class Api(View):
    @classmethod
    def as_view(cls, *args, **kwargs):
        out = super(Api, cls).as_view(*args, **kwargs)
        return json_return(
            api_output(
                out
            )
        )


class AjaxApi(LoginRequiredMixin, Api):
    pass

class SyncraeApi(Api):

    @method_decorator(http_auth_login)
    def dispatch(self, request, *args, **kwargs):
        try:
            kwargs['game'] = Game.objects.select_related().get(key=request.REQUEST.get('key', ''))
        except Game.DoesNotExist:
            kwargs['output'].error(InvalidKey('The game key is invalid, please try restarting your game session.'))

        super(SyncraeApi, self).dispatch(request, *args, **kwargs)


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
