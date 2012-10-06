from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to

from webdnd.player.views.account import AccountHomeView
from webdnd.player.views.account import LoginView
from webdnd.player.views.account import LogoutView
from webdnd.player.views.account import FriendsView
from webdnd.player.views.account import SettingsView

# API
from webdnd.player.views.account import UserSearchApi


urlpatterns = patterns('webdnd.player.views',
    url(r'^/?$', redirect_to, {'url': '/account/home'}),
    url(r'^home/?$', AccountHomeView.as_view(), name='account_home'),
    url(r'^login/?$', LoginView.as_view(), name='account_login'),
    url(r'^logout/?$', LogoutView.as_view(), name='account_logout'),
    url(r'^friends/?$', FriendsView.as_view(), name='account_friends'),
    url(r'^settings/?$', SettingsView.as_view(), name='account_settings'),

    # API
    url(r'^api/search/(?P<text>.*)$', UserSearchApi.as_view(), name="account_api_search"),
)
