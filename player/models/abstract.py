from django.db import models

class AbstractPlayerModel(models.Model):
    """
    A model for the Player tables
    """

    class Meta:
        abstract = True
        app_label = 'webdnd'