"""
Library admin site
"""

from dnd.admin.base import LibraryAdmin
from dnd.models.accounts import LibraryAccount
from dnd.models.library_entities.conditions import Condition
from dnd.models.library_entities.abilities import Ability, AbilityType
from dnd.models.library_entities.references import Article, Example, Rule, Term
from dnd.models.library_entities.skills import Skill, SkillSample
from dnd.models.library_entities.spells import CastingLevelClassPair, Spell, SpellDescriptor
from dnd.models.library_entities.classes import DnDClass
from dnd.models.units import ActionTimeDuration
from dnd.models.modifiers.saving_throws import SavingThrow
from dnd.models.modifiers.modifiers import Modifier
from dnd.models.sources import Source

DEFAULT = LibraryAdmin

library_admin_mapping = (
    (ActionTimeDuration, DEFAULT),
    (Article, DEFAULT),
    (CastingLevelClassPair, DEFAULT),
    (Condition, DEFAULT),
    (DnDClass, DEFAULT),
    (Example, DEFAULT),
    (Ability, DEFAULT),
    (AbilityType, DEFAULT),
    (LibraryAccount, DEFAULT),
    (Modifier, DEFAULT),
    (Rule, DEFAULT),
    (SavingThrow, DEFAULT),
    (Skill, DEFAULT),
    (SkillSample, DEFAULT),
    (Source, DEFAULT),
    (Spell, DEFAULT),
    (SpellDescriptor, DEFAULT),
    (Term, DEFAULT),
)

__all__ = [
    library_admin_mapping
]
