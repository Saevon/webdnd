from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.skills import SKILL_SAMPLE_TYPES
from library.models.abstract import AbstractLibraryModel
from library.models.library_entities.abstract import AbstractLibraryEntity

class Skill(AbstractLibraryEntity):
    """
    A skill.
    """

    short_description = models.TextField(blank=False)
    subtypes = models.BooleanField(blank=False)

class SkillSubType(AbstractLibraryEntity):
    """
    a subtype for a skill
        e.g. Nature for the Knowledge skill
    """

    class Meta(AbstractLibraryEntity.Meta):
        unique_together = (
            ('title','skill'),
        )

    skill = models.ForeignKey(
        Skill,
        related_field="subtypes",
        blank=False,
        null=False)

class SkillSample(AbstractLibraryModel):
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
