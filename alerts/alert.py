from django.conf import settings

from webdnd.alerts.models import Alert

class Alerts(list):

    def __init__(self, session, owner):
        super(Alerts, self).__init__(Alert.get_alerts(owner))
        self.session = session
        self.owner = owner

    def __call__(self, text, level=None, title=None, prefix=None, delay=False):
        """
        Adds a new alert to the list, if theres a delay adds it to the database
        Returns the index at which the alert is at, so you can change it afterwards
        """
        alert = Alert(
            text=text or '',
            title=title or '',
            prefix=prefix or '',
            level=level or settings.ALERT_DEFAULT_LEVEL,
            owner=self.owner
        )

        # If we're not delaying add it to the output list
        if not delay:
            alert = alert.details()
            self.append(alert)
            return len(self) - 1
        # Otherwise store it in the database for the next request
        else:
            alert.save()
            return alert

    def logout(self):
        """
        Removes any alerts for the current owner, then refreshes the
        alert_key.
        """
        Alert.clear(self.owner)
        del self[:]

        self.owner = alert_key(self.session)

def alert_key(session):
    key = session.get('alert_key', None)
    if key is None:
        session['alert_key'] = session.session_key
        key = session.session_key
    return key

def template_processor(request):
    """
    Adds the alerts to the template context
    """
    return {
        'alerts': list(request.alert),
    }
