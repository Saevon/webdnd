from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

from webdnd.shared.views import LoginRequiredMixin


def homepage(request):
    return render_to_response('game_main.html', {}, context_instance=RequestContext(request))

def display_sheet(request, character_name):
    return render_to_response('character_sheet.html', {'character_name': character_name}, context_instance=RequestContext(request))

def settings(request):
    pass

def logout(request):
    pass


class AccountHomeView(View, LoginRequiredMixin):

    def get(self, request):
        return render_to_response(
            'account/home.html',
            {},
            context_instance=RequestContext(request)
        )

class LoginView(View):

    def get(self, request):
        out = {
            'username': request.GET.get('username', ''),
            'password': '',
            # TODO: this does nothing right now, and isnt saved
            'remember': request.GET.get('remember', ''),
            'error': request.GET.get('error', False),
        }

        return render_to_response(
            'account/login.html',
            out,
            context_instance=RequestContext(request)
        )

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                url = reverse('account_home')
            else:
                # Add a page for disabled/banned users
                url = '%s?username=%s&error=1' % (reverse('account_login'), username)
        else:
            # Validation failed
            url = '%s?username=%s&error=1' % (reverse('account_login'), username)

        return HttpResponseRedirect(url)


        

