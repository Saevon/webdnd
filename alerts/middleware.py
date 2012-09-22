from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import Context, Template

from alerts.alert import Alerts, alert_key
from alerts.models import Alert

# Move this somewhere else 
class AlertMiddleware(object):

    def process_request(self, request):
        request.alert = Alerts(
            request.session,
            alert_key(request.session)
        )

