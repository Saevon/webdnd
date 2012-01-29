from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.constants.skills import SKILL_SAMPLE_TYPES
from dnd.models.abstract import AbstractDnDModel
from dnd.models.library_entities.abstract import AbstractDnDEntity

class Skill(AbstractDnDEntity):
    """
    A skill.
    """

    short_description = models.TextField(blank=False)
    has_subtypes = models.BooleanField(blank=False)

class SkillSubType(AbstractDnDEntity):
    """
    a subtype for a skill
        e.g. Nature for the Knowledge skill
    """

    class Meta(AbstractDnDEntity.Meta):
        unique_together = (
            ('title','skill'),
        )

    skill = models.ForeignKey(
        Skill,
        related_name='Skill.subtypes',
        blank=False,
        null=False)
    # (if True) always put this in the skill tree
    main = models.BooleanField(blank=False)

class SkillSample(AbstractDnDModel):
    """
    A sample skill DC or modifier that shows DC
    """

    skill = models.ForeignKey(
        Skill,
        related_name='skill_samples',
        blank=False)
    difficulty_class = models.IntegerField(blank=False, null=False)

    description = models.TextField(blank=True)
    type = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=SKILL_SAMPLE_TYPES,
        default='dc',
        blank=True)

class Language(AbstractDnDEntity):
     """docstring for Language"""

     alphabet = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=False)
