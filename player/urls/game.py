from django.conf.urls.defaults import patterns, url

from webdnd.player.views.game import CampaignView
from webdnd.player.views.game import CampaignListView
from webdnd.player.views.game import CampaignEditView
from webdnd.player.views.game import CharacterListView
from webdnd.player.views.game import CharacterEditView
from webdnd.player.views.game import PlayView


urlpatterns = patterns('webdnd.player.views',
    url(r'^campaigns/?$', CampaignListView.as_view(), name='game_campaign_list'),
    url(r'^campaign/(?P<cid>[0-9]+)/?$', CampaignView.as_view(), name='game_campaign_view'),
    url(r'^campaign/(?P<cid>[0-9]+)/edit/?$', CampaignEditView.as_view(), name='game_campaign_edit'),
    url(r'^campaign/create/?$', CampaignEditView.as_view(), {'cid': False}, name='game_campaign_create'),

    url(r'^characters/?$', CharacterListView.as_view(), name='game_character_list'),
    url(r'^character/(?P<chid>[0-9]+)/edit/?$', CharacterEditView.as_view(), name='game_character_edit'),
    url(r'^character/create/?$', CharacterEditView.as_view(), {'chid': False}, name='game_character_create'),

    # Redirect to Play view
    url(r'^campaign/(?P<cid>[0-9]+)/play/?$', PlayView.as_view(), name='game_campaign_play'),
)
