"""
Library admin site
"""

from library.admin.base import LibraryAdmin
from library.models.accounts import LibraryAccount
from library.models.library_entities.conditions import Condition
from library.models.library_entities.abilities import Ability, AbilityType
from library.models.library_entities.references import Article, Example, Rule, Term
from library.models.library_entities.skills import Skill, SkillSample
from library.models.library_entities.spells import CastingLevelClassPair, Spell, SpellDescriptor
from library.models.library_entities.classes import DnDClass
from library.models.units import ActionTimeDuration
from library.models.modifiers.saving_throws import SavingThrow
from library.models.modifiers.modifiers import Modifier
from library.models.sources import Source

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
