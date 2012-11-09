from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from webdnd.shared.views import render_to_response
from django.template import RequestContext
from django.views.generic import View
from django.contrib.auth.models import User
from django.db.models import Q

from webdnd.player.models.campaigns import Campaign
from webdnd.player.models.characters import Character
from webdnd.player.models.campaigns import Player
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
        create = not cid

        if create:
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
            'friends': request.user.friends.all(),
            'systems': Campaign.ROLEPLAYING_SYSTEMS,
            'create': create,
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
        create = not cid

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
                campaign = Campaign(owner=request.user)
                campaign.save()
                cid = campaign.id
            else:
                campaign = Campaign.objects.get(id=cid)

            campaign.name = name
            campaign.rp_system = system
            campaign.save()

            # Always add yourself to a campaign you're editing
            players.append(request.user.id)
            keep = set()
            cur_players = set(str(p.user.id) for p in campaign.players.all())
            for id in players:
                Player.objects.get_or_create(user=User.objects.get(id=id), campaign=campaign)
                keep.add(id)
            Player.objects.filter(user__id__in=cur_players - keep, campaign=campaign).delete()
            print Player.objects.filter(campaign=campaign)

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
        else:
            out = self._player(request, campaign)

        out['campaign'] = campaign,

        # Make sure syncrae knows which campaign to log you into
        request.session['cid'] = campaign.id

        return render_to_response('play.html',
            out,
            context_instance=RequestContext(request)
        )

    def _dm(self, request, campaign):
        '''
        Properties a DM requires
        '''
        player = campaign.players.get(user=request.user)

        return {
            'is_dm': True,
            'player': player,
        }

    def _player(self, request, campaign):
        '''
        Properties a Player needs
        '''
        player = campaign.players.get(user=request.user)

        # Players don't have char anymore, FIX
        char = False

        return {
            'is_dm': False,
            'player': player,
            'char': char,
        }




class CharacterListView(LoginRequiredMixin, View):
    def get(self, request):
        characters = Character.objects.filter(player__user=request.user)
        out = {
            'characters': characters,
        }
        return render_to_response('character_list.html',
            out,
            context_instance=RequestContext(request)
        )



class CharacterEditView(LoginRequiredMixin, View):
    pass
