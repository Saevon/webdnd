from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.skills import SKILL_SAMPLE_TYPES
from library.models.library_entities.abstract import AbstractLibraryEntity

class Skill(AbstractLibraryEntity):
    """
    A skill.
    """

    short_description = models.TextField(blank=False)

class SkillSample(models.Model):
    """
    A sample skill DC or modifier that shows DC
    """
    
    skill = models.ForeignKey(Skill, blank=False)
    difficulty_class = models.IntegerField(blank=False, null=False)

    description = models.TextField(blank=True)
    type = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=SKILL_SAMPLE_TYPES,
        default='dc',
        blank=True)
