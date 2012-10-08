from django.conf.urls.defaults import patterns, url

from webdnd.player.views.account import UserSearchApi
from webdnd.player.views.account import UserDetailsApi

urlpatterns = patterns('webdnd.player.views',
    # Account
    url(r'^account/search/(?P<text>.*)/?$', UserSearchApi.as_view(), name="account_api_search"),
    url(r'^account/user/self/?$', UserDetailsApi.as_view(), name="account_api_user_self"),
)
