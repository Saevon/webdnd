from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to


urlpatterns = patterns('webdnd.player.views',
    url(r'^$', redirect_to, {'url': '/account/login'}),
    url(r'^login', 'login'),
    url(r'^logout', 'logout'),
    url(r'^settigs', 'settings'),
)
