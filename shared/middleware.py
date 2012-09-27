from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed

from BeautifulSoup import BeautifulSoup


class HtmlPrettifyMiddleware(object):
    """
    HTML code prettification middleware.
    """

    def __init__(self, *args, **kwargs):
        if not settings.PRETTIFY_HTML:
            raise MiddlewareNotUsed

    def process_response(self, request, response):
        if response['Content-Type'].split(';', 1)[0] == 'text/html':
            response.content = BeautifulSoup(response.content).prettify()
        return response