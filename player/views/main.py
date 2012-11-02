from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.http import HttpResponse, HttpResponseRedirect
from webdnd.shared.views import render_to_response
from django.template import RequestContext
from django.views.generic import View
from django.contrib.auth.models import User


class HomeView(View):
    def get(self, request):
        out = {
            'total_users': User.objects.count(),
        }
        return render_to_response(
            'home.html',
            out,
            context_instance=RequestContext(request)
        )

    def post(self, request):
        if request.POST.get('newsletter_submit'):
            email = request.POST.get('newsletter_email')
            if not email is None or not email_re.match(email):
                request.highlight('#group-email', text='Please enter an email')
            return self.get(request)




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
