from django.conf.urls.defaults import *
from django.conf import settings

# from game.views import *
from dnd.views import *

from django.contrib import admin
from lib.admin import register_mapping
#from game.admin.mapping import game_admin_mapping
#from game.admin.site import GameAdminSite
from dnd.admin import library_admin_mapping
from dnd.admin.site import LibraryAdminSite

# General admin
register_mapping(admin.site.register, library_admin_mapping)#, game_admin_mapping)
admin.autodiscover()

#Library Admin
library_admin_site = LibraryAdminSite()
register_mapping(library_admin_site.register, library_admin_mapping)

#Game Admin
#game_admin_site = GameAdminSite()
#register_mapping(game_admin_site.register, game_admin_mapping)

urlpatterns = patterns('',
    # Example:[A-Za-z]
    # (r'^webdnd/', include('web_dnd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # (r'^game/$', homepage),
    # (r'^charsheet/([A-Za-z]*)$', display_sheet),
    (r'^library/$', library_home),

    # Uncomment the next lines to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^game-admin/', include(game_admin_site.urls)),
    (r'^library-admin/', include(library_admin_site.urls)),
)

# for serving static files in development evnironment only
if settings.DEBUG:
    from os.path import expanduser
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': expanduser("~/code/webdnd/media")}),
        # (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': expanduser("~/Developer/webdnd/media")}),
    )
