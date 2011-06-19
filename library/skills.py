from django.db import models
from library.constants import *
from library.abstract_models import *

class Skill(models.Model):
    """
    A skill.
    """

    short_description = models.TextField(blank=False)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"Skill"

class SkillSample(models.Model):
    """
    A sample skill DC or modifier that shows DC
    """
    
    skill = models.ForeignKey('Skill', blank=False)
    difficulty_class = models.IntegerField(blank=False, null=False)
    type = models.CharField(
        blank=False,
        max_length=STND_ID_CHAR_LIMIT,
        choices=SKILL_SAMPLE_TYPES,
        default=SKILL_SAMPLE_TYPES[0]))

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"SkillSample"
