from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

from webdnd.player.views import AccountHomeView
from webdnd.player.views import LoginView
from webdnd.player.views import LogoutView


urlpatterns = patterns('webdnd.player.views',
    url(r'^$', redirect_to, {'url': '/account/login'}),
    url(r'^home$', AccountHomeView.as_view(), name='account_home'),
    url(r'^login', LoginView.as_view(), name='account_login'),
    url(r'^logout', LogoutView.as_view(), name='account_logout'),
    url(r'^settings', 'settings', name='account_settings'),
)
