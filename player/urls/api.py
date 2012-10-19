from django.conf.urls.defaults import patterns, url

from webdnd.player.views.account import UserSearchApi
from webdnd.player.views.terminal import TerminalSearchApi

urlpatterns = patterns('webdnd.player.views',
    # Account
    url(r'^account/search/(?P<text>.*)/?$', UserSearchApi.as_view(), name="account_api_search"),
    url(r'^terminal/search/?$', TerminalSearchApi.as_view(), name="terminal_api_search"),
)
