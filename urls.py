from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^account/', include('webdnd.player.urls.account')),
    url(r'^game/', include('webdnd.player.urls.game')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # (r'^charsheet/([A-Za-z]*)$', display_sheet),
    # (r'^library/$', library_home),

    # Uncomment the next lines to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Main homepage
    url(r'', include('webdnd.player.urls.main')),
) + staticfiles_urlpatterns()

# Page to serve in case one of these errors occurs
# handler404 = 'webdnd.views.main.error_404'
# handler403 = 'webdnd.views.main.error_403'
# handler500 = 'webdnd.views.main.error_500'

# for serving static files in development evnironment only
if settings.DEBUG:
    from os.path import expanduser
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': expanduser(settings.MEDIA_ROOT)}),
    )
