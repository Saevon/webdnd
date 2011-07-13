from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.library_entities.abstract import AbstractLibraryEntity

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
