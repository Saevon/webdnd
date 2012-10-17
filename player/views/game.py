from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View
from django.contrib.auth.models import User
from django.db.models import Q

from webdnd.player.constants.campaign import ROLEPLAYING_SYSTEMS
from webdnd.player.models.campaigns import Campaign
from webdnd.player.models.players import Player
from webdnd.shared.views import LoginRequiredMixin


class CampaignListView(LoginRequiredMixin, View):
    def get(self, request):
        out = {
            'campaigns': my_campaigns(request.user),
        }
        return render_to_response(
            'campaign_list.html',
            out,
            context_instance=RequestContext(request)
        )

def my_campaigns(user):
    # Get all players that represent you
    players = Player.objects.filter(user=user)

    # Get all campaigns you can see, you own them or you play
    # in them
    campaigns = Campaign.objects.filter(
        Q(owner=user)
        | Q(id__in=[p.campaign.id for p in players])
    )

    return campaigns


class CampaignView(LoginRequiredMixin, View):
    def get(self, request, cid):
        campaign = Campaign.objects.get(id=cid)
        players = set(campaign.players.all())

        out = {
            'players': players,
            'campaign': campaign,
        }

        return render_to_response(
            'campaign_view.html',
            out,
            context_instance=RequestContext(request)
        )


class CampaignEditView(LoginRequiredMixin, View):
    def get(self, request, cid):
        created = not cid

        if created:
            players = []
            campaign = {
                'name': '',
                'rp_system': 'D&D 3.5',
            }
        else:
            campaign = Campaign.objects.get(id=cid)
            players = set(p.user.id for p in campaign.players.all())

        out = {
            'players': players,
            'friends': request.user.friends.exclude(id=request.user.id),
            'systems': ROLEPLAYING_SYSTEMS,
            'create': created,
            'campaign': campaign,
        }

        return render_to_response(
            'campaign_edit.html',
            out,
            context_instance=RequestContext(request)
        )

    def post(self, request, cid):
        name = request.POST.get('name')
        system = request.POST.get('system')
        players = request.POST.getlist('players[]')
        create = bool(cid)

        # validation
        change = True
        if not name:
            request.highlight('#group-name', text='Campaign name is a required field.')
            change = False
        if not system:
            request.highlight('#group-system', text='A roleplaying system is required.')
            change = False

        if change:
            if create:
                campaign = Campaign.objects.get(id=cid)
            else:
                campaign = Campaign(owner=request.user)
                campaign.save()
                cid = campaign.id

            campaign.name = name
            campaign.rp_system = system
            campaign.save()

            cur_players = set(str(p.user.id) for p in campaign.players.all())
            keep = set()
            for id in players:
                Player.objects.get_or_create(user=User.objects.get(id=id), campaign=campaign)
                keep.add(id)
            Player.objects.filter(user__id__in=cur_players - keep, campaign=campaign).delete()

            text = 'Your changes have been saved.'
            if create:
                text = 'A new campaign was created.'

            request.alert(
                prefix='Alright!',
                text=text,
                level='success'
            )
        else:
            request.alert(
                title='Not Saved!.',
                prefix='Try Again!',
                text='There were some problems with your input.',
                level='error'
            )

        if create and change:
            return HttpResponseRedirect(reverse('game_campaign_edit', kwargs={'cid': cid}))

        return self.get(request, cid)

class PlayView(LoginRequiredMixin, View):

    def get(self, request, cid):
        campaign = Campaign.objects.get(id=cid)

        if request.user == campaign.owner:
            out = self._dm(request, campaign)
            out['is_dm'] = True
        else:
            out = self._player(request, campaign)
            out['is_dm'] = False

        out['campaign'] = campaign,

        # Make sure syncrae know which campaign to log you into
        request.session['cid'] = campaign.id

        return render_to_response('play.html',
            out,
            context_instance=RequestContext(request)
        )

    def _dm(self, request, campaign):

        return {

        }

    def _player(self, request, campaign):
        player = campaign.players.get(user=request.user)

        if player.cur_char and player.cur_char.status != 'Dead':
            char = player.cur_char
        else:
            char = False

        return {
            'player': player,
            'char': char,
        }




