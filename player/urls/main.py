from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

from webdnd.player.views.main import HomeView
from webdnd.player.views.main import AboutView
from webdnd.player.views.main import ContactView


urlpatterns = patterns('webdnd.player.views.main',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about', AboutView.as_view(), name='about'),
    url(r'^contact_us', ContactView.as_view(), name='contact_us'),
)
