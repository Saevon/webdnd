from django.conf.urls.defaults import patterns, url

from webdnd.player.views.account import UserSearchApi


urlpatterns = patterns('webdnd.player.views',
    # Account
    url(r'^account/search/(?P<text>.*)$', UserSearchApi.as_view(), name="account_api_search"),

    # Game
    url(r'^game/', UserSearchApi.as_view(), name="account_api_search"),
)
