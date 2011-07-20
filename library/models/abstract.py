from django.db import models

class AbstractLibraryModel(models.Model):
    """
    A model within the Library App
    """
    
    class Meta:
        abstract = True
        app_label = 'library'
