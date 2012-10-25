from django.conf import settings

from alerts.models import Alert


class Alerts(list):

    def __init__(self, session, owner):
        super(Alerts, self).__init__(Alert.get_alerts(owner))
        self.session = session
        self.owner = owner

    def __call__(self, text, level=None, title=None, prefix=None, important=None):
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
        if important is None:
            important = level in settings.ALERT_IMPORTANT_LEVELS
        alert.closable = not important

        self.append(alert)
        return alert

    def logout(self):
        """
        Removes any alerts for the current owner, then refreshes the
        alert_key.
        """
        Alert.clear(self.owner)
        del self[:]

        self.owner = alert_key(self.session)

    def delay(self):
        """
        Removes any alerts that are being shown, delaying them for the next call
        """
        for alert in self:
            alert.save()
        self[:] = []

    def process(self):
        return [alert.details() for alert in self]


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
        'alerts': request.alert.process(),
    }
