from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, Template
from django.template import RequestContext

from alerts.alert import Alerts, alert_key
from alerts.models import Alert
from alerts.highlighter import Highlighter


class AlertMiddleware(object):
    """
    A Middleware used to add notifications and alerts to the current user
    """

    def process_request(self, request):
        """
        Adds the alert interface into the request
        """
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

class FieldHighlightMiddleware(object):
    """
    A Middleware used to highlight fields based on input validation
    """

    def process_request(self, request):
        """
        Adds the highlight interface into the request
        """
        request.highlight = Highlighter()

