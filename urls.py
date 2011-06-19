from django.conf.urls.defaults import *
from django.conf import settings

# from game.views import *
from library.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:[A-Za-z]
    # (r'^webdnd/', include('web_dnd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # (r'^game/$', homepage),
    # (r'^charsheet/([A-Za-z]*)$', display_sheet), 
    (r'^library/$', library_home), 

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

# for serving static files in development evnironment only
if settings.DEBUG:
    from os.path import expanduser
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': expanduser("~/code/webdnd/media")}),
        # (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': expanduser("~/Developer/webdnd/media")}),
    )
