from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.models.abstract import AbstractDnDModel
from dnd.models.library_entities.abstract import AbstractDnDEntity

class Rule(AbstractDnDEntity):
    """
    A rule.

    * may containt Terms
    * may "spawn" Terms
    """

    examples = models.ManyToManyField(
        'Example',
        related_name="rules",
        blank=True)
    body = models.TextField(blank=False)

class Term(AbstractDnDEntity):
    """
    A glossary term. Usually spawned from a Rule
    """

    short_description = models.TextField(blank=False)
    examples = models.ManyToManyField(
        'Example',
        related_name="terms",
        blank=True)
    rule = models.ForeignKey(
        Rule,
        related_name="terms",
        blank=True)
    # Note when adding a new term we should ensure it gets an alias added
    # This way we only have to search aliases for the different terms

    def get_aliases(self):
        """
        Returns all the ames for this term.
        """
        return [alias.name for alias in self.aliases]

class Alias(AbstractDnDModel):
    """
    An alias for a Term.
    """

    name = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=False,
        unique=True)
    term = models.ForeignKey(
        Term,
        related_name="aliases",
        blank=False)

class Article(AbstractDnDEntity):
    """
    An article about various D&D stuff, NOT a Rule.
    """

    examples = models.ManyToManyField(
        'Example',
        related_name="articles",
        blank=True)

class Example(AbstractDnDEntity):
    """
    An example of a rule.
    """
