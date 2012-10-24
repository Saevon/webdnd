from django.conf import settings
from django.contrib.auth.models import User

from shared.utils.index import WhooshIndex
from whoosh.qparser import MultifieldParser, RegexPlugin
from whoosh.query import Regex
from whoosh.fields import Schema
from whoosh.fields import ID, TEXT
from whoosh.sorting import FieldFacet
import re


class UserIndex(WhooshIndex):

    CLASSES = {
        'all': ['User']
    }

    def schema(self):
        return Schema(
            id=ID(unique=True, stored=True),
            username=TEXT(stored=True),
            name=TEXT(stored=True),
        )

    def index_data(self, item):
        """
        Converts the item into an indexable dictionary
        """
        return {
            'id': unicode(item.id),
            'username': unicode(item.username),
            'name': unicode(item.name),
        }

    def refresh_list(self):
        return User.objects.all()

    def search(self, text):
        # escape any possible regexp chars
        text = re.escape(text)

        # Use Regexp to imitate fuzzy search
        # Remove any non-name characters
        text = settings.USER_CHAR_RE.sub('', text)
        # Add regexp syntax to fake Fuzzy Search
        # The r" ... " is Whoosh syntax meaning 'the following is a regexp'
        text = 'r".*%s.*"' % ('.*'.join(text))

        with self.index.searcher() as searcher:
            query = (MultifieldParser([u'username', u'name'], self.index.schema, termclass=Regex)
            )
            query.add_plugin(RegexPlugin)
            query = query.parse(unicode(text))

            sort = FieldFacet(u'name')

            results = searcher.search(query, limit=20, sortedby=sort)

            out = []
            for r in results:
                out.append({
                    'id': r['id'],
                    'username': r['username'],
                    'name': r['name'],
                })

            return out

from django.db import models
from django.dispatch import receiver



@receiver(models.signals.post_save)
def update_index(sender, instance, created, **kwargs):
    if type(instance).__name__ in UserIndex.CLASSES['all']:
        UserIndex.get(settings.USER_INDEX_DIR).refresh_item(instance)

@receiver(models.signals.post_delete)
def delete_index(sender, instance, **kwargs):
    if type(instance).__name__ in WhooshIndex.CLASSES['all']:
        UserIndex.get(settings.USER_INDEX_DIR).delete_item(instance)
