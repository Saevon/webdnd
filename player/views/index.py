from django.conf import settings
from django.contrib.auth.models import User

from shared.utils.index import WhooshIndex
from whoosh import index
from whoosh.qparser import MultifieldParser, OrGroup, QueryParser
from whoosh.query import Term
from whoosh.fields import Schema
from whoosh.fields import ID, TEXT


class UserIndex(WhooshIndex):

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
        text = '*%s*' % text

        with self.index.searcher() as searcher:
            query = (MultifieldParser([u'username', u'name'], self.index.schema)
                .parse(unicode(text))
            )

            results = searcher.search(query, limit=20)

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
def update_index(sender, instance, **kwargs):
    if type(instance).__name__ in UserIndex.CLASSES['all']:
        index = UserIndex.get(settings.USER_INDEX_DIR).refresh_item(instance)

@receiver(models.signals.post_delete)
def delete_index(sender, instance, **kwargs):
    if type(instance).__name__ in WhooshIndex.CLASSES['all']:
        index = UserIndex.get(settings.USER_INDEX_DIR).delete_item(instance)
