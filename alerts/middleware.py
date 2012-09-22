from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import Context, Template
from django.http import HttpResponseRedirect

from alerts.alert import Alerts, alert_key
from alerts.models import Alert

# Move this somewhere else 
class AlertMiddleware(object):

    def process_request(self, request):
        request.alert = Alerts(
            request.session,
            alert_key(request.session)
        )

    def process_response(self, request, response):
        """
        Delays any messages if this view redirects you
        """
        if isinstance(response, HttpResponseRedirect):
            # Force delay any current messages
            request.alert.delay()
        return response