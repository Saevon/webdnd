from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

def library_home(request):
    return render_to_response('library_main.html', {}, context_instance=RequestContext(request))
