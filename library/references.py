from django.db import models
from library.constants import *
from library.abstract_models import *

class Rule(AbstractLibraryEntity):
    """
    A rule.
    
    * may containt Terms
    * may "spawn" Terms
    """
    
    examples = models.ManyToManyField("Example", related_name='rules', blank=True)
    body = models.TextField(blank=False)
    
    class Admin:
        list_display = ("",)
        search_fields = ("",)

    def __unicode__(self):
        return self.title

class Term(AbstractLibraryEntity):
    """
    A glossary term.
    """
    
    short_description = models.TextField(blank=False)
    examples = models.ManyToManyField("Example", related_name='terms', blank=True)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"Term"

class Article(models.Model):
    """
    An article about various D&D stuff, NOT a Rule.
    """
    
    examples = models.ManyToManyField("Example", related_name='articles', blank=True)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"Article"


class Example(AbstractLibraryEntity):
    """
    An example of a rule.
    """
    
    class Admin:
        list_display = ("",)
        search_fields = ("",)

    def __unicode__(self):
        return self.title
