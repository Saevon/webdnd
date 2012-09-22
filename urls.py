from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import redirect_to

# from player.admin.mapping import game_admin_mapping
# from player.admin.site import GameAdminSite
# from dnd.admin import library_admin_mapping
# from dnd.admin.site import LibraryAdminSite

# General admin
# register_mapping(
#     admin.site.register,
#     library_admin_mapping,
#     game_admin_mapping,
# )
admin.autodiscover()

#Library Admin
# library_admin_site = LibraryAdminSite()
# register_mapping(library_admin_site.register, library_admin_mapping)

#Game Admin
# game_admin_site = GameAdminSite()
# register_mapping(game_admin_site.register, game_admin_mapping)

urlpatterns = patterns('',
    url(r'^account/', include('webdnd.player.urls.account')),

    # Example:[A-Za-z]
    # (r'^webdnd/', include('web_dnd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # (r'^game/$', homepage),
    # (r'^charsheet/([A-Za-z]*)$', display_sheet),
    # (r'^library/$', library_home),

    # Uncomment the next lines to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # (r'^game-admin/', include(game_admin_site.urls)),
    # (r'^library-admin/', include(library_admin_site.urls)),
    url(r'', include('webdnd.player.urls.main')),
) + staticfiles_urlpatterns()

# Page to serve in case one of these errors occurs
# handler404 = '.views.error_404'
# handler403 = '.views.error_403'
# handler500 = '.views.error_500'

# for serving static files in development evnironment only
if settings.DEBUG:
    from os.path import expanduser
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': expanduser(settings.MEDIA_ROOT)}),
    )
