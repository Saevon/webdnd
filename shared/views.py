from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
    """
    Mixin that requires all methods for this view to have a logged in user
    """

    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())

