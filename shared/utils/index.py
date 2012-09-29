from shared.utils.decorators import cascade
from whoosh import index
import os


class WhooshIndex(object):

    CLASSES = {
        'all': []
    }

    INDICES = {}

    def __init__(self, indexdir):
        """
        Creates a new index that reads/writes into the folder indexdir
            Do NOT create WhooshIndexes directly, use the get method
        """
        self._indexdir = indexdir
        self._writer = None

    @classmethod
    def get(cls, indexdir=None, flush=False):
        """
        Returns the WhooshIndex that is reading the index located in the
        indexdir folder. flush indicates whether the index should be
        remade from scratch, however this doesn't happen if the index is
        already open.
        """
        if not indexdir in WhooshIndex.INDICES:
            WhooshIndex.INDICES[indexdir] = (cls(indexdir)
                .open_index(flush=flush)
            )

        return WhooshIndex.INDICES[indexdir]

    @cascade
    def create_schema(self, flush=False):
        """
        Creates the Schema for the index. if flush is True this removes
        the old index if there was one.
        """
        from shutil import rmtree

        schema = self.schema()

        # Remove the old index if flushing
        if flush:
            rmtree(self._indexdir)

        # Create the folder if needed
        if not os.path.exists(self._indexdir):
            os.makedirs(os.path.abspath(self._indexdir))

        # make the actual index
        self.index = index.create_in(self._indexdir, schema)
        self.refresh()

    @cascade
    def open_index(self, flush=False):
        """
        Opens the index for reading/writing
        """
        if not os.path.exists(self._indexdir) or flush:
            self.create_schema(flush=flush)
        else:
            self.index = index.open_dir(self._indexdir)

    @cascade
    def refresh_item(self, item):
        """
        creates/updates the index for this item.
        """
        writer = self.index.writer()
        writer.update_document(**self.index_data(item))
        writer.commit()

    @cascade
    def delete_item(self, item):
        """
        Deletes the item from the index
        """
        writer = self.index.writer()
        data = self.index_data(item)
        writer.delete_by_term(u'index_id', data['index_id'])
        writer.commit()

    def schema(self):
        """
        Returns a valid whoosh schema
        """
        raise NotImplementedError

    @cascade
    def refresh(self):
        writer = self.index.writer()

        for item in self.refresh_list():
            data = self.index_data(item)
            writer.update_document(**data)
        writer.commit()

    def search(self, *args, **kwargs):
        raise NotImplementedError

    def index_data(self, item, *args, **kwargs):
        raise NotImplementedError

"""
from django.db import models
from django.dispatch import receiver


@receiver(models.signals.post_save)
def update_index(sender, instance, **kwargs):
    if type(instance).__name__ in WhooshIndex.CLASSES['all']:
        index = WhooshIndex.get(settings.INDEX_DIR).refresh_item(instance)

@receiver(models.signals.post_delete)
def delete_index(sender, instance, **kwargs):
    if type(instance).__name__ in WhooshIndex.CLASSES['all']:
        index = WhooshIndex.get(settings.INDEX_DIR).delete_item(instance)
"""
