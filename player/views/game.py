from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View
from django.contrib.auth.models import User

from webdnd.player.constants.campaign import ROLEPLAYING_SYSTEMS
from webdnd.player.models.campaigns import Campaign
from webdnd.player.models.campaigns import Game
from webdnd.player.models.players import Player
from webdnd.shared.views import LoginRequiredMixin

class CampaignListView(LoginRequiredMixin, View):
    def get(self, request):
        campaigns = Campaign.objects.filter(owner=request.user)

        out = {
            'campaigns': campaigns,
        }
        return render_to_response(
            'campaign_list.html',
            out,
            context_instance=RequestContext(request)
        )

class CampaignView(LoginRequiredMixin, View):
    def get(self, request):
        return render_to_response(
            'campaign.html',
            {},
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
            'systems': [i[1] for i in ROLEPLAYING_SYSTEMS],
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
            campaign.system = system
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
        if (not campaign.players.filter(user=request.user).count()
            or campaign.owner == request.user):
            # Not allowed, error out
            pass

        # Delete any old sesions
        Game.objects.filter(user=request.user).delete()

        # Create the game session
        game = Game(user=request.user, campaign=campaign)
        game.new_key()
        game.save()

        # Current redirect to the tornado app, needs to be fixed up for deployment
        # See line below for the actual url
        return HttpResponseRedirect(':8888/play?cid=%(cid)s&uid=%(uid)i&key=%(key)s' % {
            'cid': cid,
            'uid': request.user.id,
            'key': game.key,
        })

        # Actual tornado redirect
        return HttpResponseRedirect('/play?cid=%(cid)s&uid=%(uid)i&key=%(key)s' % {
            'cid': cid,
            'uid': request.user.id,
            'key': game.key,
        })


