from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

def homepage(request):
    return render_to_response('game_main.html', {}, context_instance=RequestContext(request))

def display_sheet(request, character_name):
    return render_to_response('character_sheet.html', {'character_name': character_name}, context_instance=RequestContext(request))
