from django.conf import settings

from webdnd.shared.views import AjaxApi
from webdnd.player.views.index import TerminalIndex


class TerminalSearchApi(AjaxApi):
    def get(self, request, output):
        text = request.GET.get('text')
        uid = request.GET.get('uid')
        cid = request.GET.get('cid')
        by_time = request.GET.get('by_time', True)

        results = TerminalIndex.get(TerminalIndex.get_loc(uid=uid, cid=cid)).search(text, by_time=by_time)

        output.output(results)

