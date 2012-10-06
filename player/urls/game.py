from django.conf.urls.defaults import patterns, url

from webdnd.player.views.game import CampaignView
from webdnd.player.views.game import CampaignListView
from webdnd.player.views.game import CampaignEditView


urlpatterns = patterns('webdnd.player.views',
    url(r'^campaigns/?$', CampaignListView.as_view(), name='game_campaign_list'),
    url(r'^campaign/(?P<cid>[0-9]+)/?$', CampaignView.as_view(), name='game_campaign_view'),
    url(r'^campaign/(?P<cid>[0-9]+)/edit/?$', CampaignEditView.as_view(), name='game_campaign_edit'),
    url(r'^campaign/create/?$', CampaignEditView.as_view(), {'cid': False}, name='game_campaign_create'),
)
