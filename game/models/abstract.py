from django.db import models

class AbstractGameModel(models.Model):
    """
    A model within the Game App
    """

    class Meta:
        abstract = True
        app_label = 'game'