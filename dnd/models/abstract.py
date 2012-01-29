from django.db import models

class AbstractDnDModel(models.Model):
    """
    A model for the Dnd tables
    """

    class Meta:
        abstract = True
        app_label = 'webdnd'