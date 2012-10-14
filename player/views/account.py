from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View

from webdnd.shared.views import LoginRequiredMixin
from webdnd.shared.utils.quotes import blurb
from webdnd.shared.views import AjaxApi
from webdnd.shared.views import SyncraeApi

from webdnd.player.views.index import UserIndex
from webdnd.player.views.game import my_campaigns


class AccountHomeView(LoginRequiredMixin, View):

    def get(self, request):
        campaigns = my_campaigns(request.user)

        return render_to_response(
            'account/home.html',
            {
                'campaigns': campaigns,

            },
            context_instance=RequestContext(request)
        )

class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        out = {
            'friends': request.user.friends.exclude(id=request.user.id)
        }
        return render_to_response(
            'account/friends.html',
            out,
            context_instance=RequestContext(request)
        )

    def post(self, request):
        friends = set(f.id for f in request.user.friends.all())
        unfriends = set(int(f) for f in request.POST.getlist('unfriends[]'))
        new_friends = set(int(f) for f in request.POST.getlist('new-friends[]'))

        final_friends = (friends - unfriends) | new_friends

        request.user.friends = User.objects.filter(id__in=final_friends)
        request.user.save()

        request.alert(
            prefix='Alright!',
            text='Your changes have been saved',
            level='success'
        )

        return HttpResponseRedirect(reverse('account_friends'))


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

        return HttpResponseRedirect(reverse('account_settings'))


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
            'next': request.GET.get('next', ''),
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
                url = request.POST.get('next', None)
                if not url:
                    url = reverse('account_home')

                prefix = 'Welcome %s!' % (user.get_full_name())
                request.alert(blurb('welcome'), prefix=prefix, title='Logged in', level='success')
            else:
                request.alert(title='Banned Account', prefix='Sorry,', text='This account appears to be banned', level='error')
                url = '%s?username=%s' % (reverse('account_login'), username)
        else:
            request.alert(title='Login Failed', text='Please check your credentials and try agin.', level='error')
            request.highlight('#group-pass')
            request.highlight('#group-username')

            return self.get(request)

        return HttpResponseRedirect(url)



################
# API Calls
################

class UserSearchApi(AjaxApi):

    def get(self, request, text, output):
        results = UserIndex.get(settings.USER_INDEX_DIR).search(text)

        output.output(results)


# Syncrae

class UserDetailsApi(SyncraeApi):

    def get(self, request, output, game):
        output.output({
            'name': game.user.name,
            'is_dm': (game.user == game.campaign.owner),
            'campaign_name': game.campaign.name,
        })





