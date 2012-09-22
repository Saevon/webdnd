from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View


class HomeView(View):
    def get(self, request):
        return render_to_response(
            'home.html',
            {},
            context_instance=RequestContext(request)
        )

class AboutView(View):
    def get(self, request):
        return render_to_response(
            'home.html',
            {},
            context_instance=RequestContext(request)
        )

class ContactView(View):
    def get(self, request):
        return render_to_response(
            'home.html',
            {},
            context_instance=RequestContext(request)
        )
