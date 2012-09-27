from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View

from webdnd.player.models.campaigns import Campaign
from webdnd.shared.views import LoginRequiredMixin
from webdnd.shared.utils.quotes import blurb


class AccountHomeView(LoginRequiredMixin, View):

    def get(self, request):
        campaigns = Campaign.objects.filter(owner=request.user)

        return render_to_response(
            'account/home.html',
            {
                'campaigns': campaigns,

            },
            context_instance=RequestContext(request)
        )


class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        out = {}
        return render_to_response(
            'account/settings.html',
            out,
            context_instance=RequestContext(request)
        )

    def post(self, request):
        if 'update-password' in request.POST:
            return self.update_password(request)

    def update_password(self, request):
        password = request.POST.get('password')
        new_password = request.POST.get('new-password')
        repeat_password = request.POST.get('new-password-2')

        change = True
        if not request.user.check_password(password):
            request.highlight('#group-old-pass', text='Incorrect password.')
            change = False
        if new_password != repeat_password:
            request.highlight('#group-new-pass', text='Passwords don\'t match')
            change = False
        elif new_password == '' or repeat_password == '':
            request.highlight('#group-new-pass', text='Empty passwords not allowed')
            change = False

        if change:
            request.user.set_password(new_password)
            request.user.save()

            request.alert(
                prefix='Alright!',
                text='Your new password hs been updated.',
                level='success'
            )
        else:
            request.alert(
                title='Password NOT Changed.',
                prefix='Try Again!',
                text='There were some problems with your input.',
                level='error'
            )

        return self.get(request)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        request.alert.logout()

        request.alert('You have successfully logged out', prefix='Yay!', level='success')

        return HttpResponseRedirect(reverse('account_login'))

class LoginView(View):
    def get(self, request):
        out = {
            'username': request.GET.get('username', ''),
            'password': '',
            # TODO: this does nothing right now, and isnt saved
            'remember': request.GET.get('remember', ''),
        }
        if request.user.is_authenticated():
            out['username'] = request.user.username
            request.alert('You are already logged in', level='info')

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

                prefix = 'Welcome %s!' % (user.get_full_name())
                request.alert(blurb('welcome'), prefix=prefix, title='Logged in', level='success')
            else:
                request.alert(title='Banned Account', prefix='Sorry,', text='This account appears to be banned', level='error')
                url = '%s?username=%s' % (reverse('account_login'), username)
        else:
            request.alert(title='Login Failed', text='Please check your credentials and try agin.', level='warning')
            url = '%s?username=%s' % (reverse('account_login'), username)

        return HttpResponseRedirect(url)


