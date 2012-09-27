from django.conf import settings

from BeautifulSoup import BeautifulSoup


class PrettifyMiddleware(object):
    """
    HTML code prettification middleware.
    Prettifies HTML only if you're debugging
    """

    # # TODO: Move debug check to __init__, so that it only happens once
    # def __init__(self), *args, **kwargs):
        # pass

    def process_response(self, request, response):
        if settings.DEBUG and response['Content-Type'].split(';', 1)[0] == 'text/html':
            response.content = BeautifulSoup(response.content).prettify()
        return response