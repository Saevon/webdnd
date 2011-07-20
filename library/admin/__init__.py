"""
Library admin site
"""

from library.admin.base import LibraryAdmin
from library.models.accounts import LibraryAccount
from library.models.library_entities.conditions import Condition
from library.models.library_entities.feats import Feat, FeatType
from library.models.library_entities.references import Article, Example, Rule, Term
from library.models.library_entities.skills import Skill, SkillSample
from library.models.library_entities.spells import CastingLevelClassPair, Spell, SpellDescriptor, SpellRange, SpellSubSchool
from library.models.library_entities.unknown import ActionTimeDuration, DnDClass, SavingThrow
from library.models.modifiers.modifiers import Modifier
from library.models.sources import Source

DEFAULT = LibraryAdmin

library_admin_mapping = (
    (ActionTimeDuration, DEFAULT),
    (Article,DEFAULT),
    (CastingLevelClassPair, DEFAULT),
    (Condition,DEFAULT),
    (DnDClass, DEFAULT),
    (Example,DEFAULT),
    (Feat,DEFAULT),
    (FeatType,DEFAULT),
    (LibraryAccount, DEFAULT),
    (Modifier, DEFAULT),
    (Rule,DEFAULT),
    (SavingThrow, DEFAULT),
    (Skill,DEFAULT),
    (SkillSample,DEFAULT),
    (Spell, DEFAULT),
    (SpellDescriptor, DEFAULT),
    (SpellRange, DEFAULT),
    (SpellSubSchool, DEFAULT),
    (Source, DEFAULT),
    (Term,DEFAULT),
)

__all__ = [
    library_admin_mapping
]
