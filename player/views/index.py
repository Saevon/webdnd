from django.conf import settings
from django.contrib.auth.models import User

from shared.utils.index import WhooshIndex
from whoosh.qparser import MultifieldParser
from whoosh.query import FuzzyTerm
from whoosh.fields import Schema
from whoosh.fields import ID, TEXT

def fuzzy(*args, **kwargs):
    kwargs['prefixlength'] = 0
    kwargs['maxdist'] = 10
    return FuzzyTerm(*args, **kwargs)

class UserIndex(WhooshIndex):

    CLASSES = {
        'all': [User]
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
        with self.index.searcher() as searcher:
            query = (MultifieldParser([u'username', u'name'], self.index.schema, termclass=fuzzy)
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
        UserIndex.get(settings.USER_INDEX_DIR).refresh_item(instance)

@receiver(models.signals.post_delete)
def delete_index(sender, instance, **kwargs):
    if type(instance).__name__ in WhooshIndex.CLASSES['all']:
        UserIndex.get(settings.USER_INDEX_DIR).delete_item(instance)
