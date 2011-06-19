from django.db import models
from library.constants import *
from library.abstract_models import *

class Rule(AbstractLibraryEntity):
    """
    A rule.
    
    * may containt Terms
    * may "spawn" Terms
    """
    
    examples = models.ManyToManyField("Example", related_name="rules", blank=True)
    body = models.TextField(blank=False)

class Term(AbstractLibraryEntity):
    """
    A glossary term.
    """
    
    short_description = models.TextField(blank=False)
    examples = models.ManyToManyField("Example", related_name="terms", blank=True)

class Article(AbstractLibraryEntity):
    """
    An article about various D&D stuff, NOT a Rule.
    """
    
    examples = models.ManyToManyField("Example", related_name="articles", blank=True)

class Example(AbstractLibraryEntity):
    """
    An example of a rule.
    """
