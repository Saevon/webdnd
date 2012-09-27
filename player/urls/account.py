from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

from webdnd.player.views.account import AccountHomeView
from webdnd.player.views.account import LoginView
from webdnd.player.views.account import LogoutView
from webdnd.player.views.account import SettingsView


urlpatterns = patterns('webdnd.player.views',
    url(r'^$', redirect_to, {'url': '/account/home'}),
    url(r'^home', AccountHomeView.as_view(), name='account_home'),
    url(r'^login', LoginView.as_view(), name='account_login'),
    url(r'^logout', LogoutView.as_view(), name='account_logout'),
    url(r'^settings', SettingsView.as_view(), name='account_settings'),
)