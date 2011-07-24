"""
Magic related Constants
"""

AURA_STRENGTHS = (
   ("dim", "Dim"),
   ("fnt", "Faint"),
   ("mod", "Moderate"),
   ("strng", "Strong"),
   ("op", "Overpowering"),
)

MAGIC_SOURCES = (
    ('arc', 'Arcane'),
    ('div', 'Divine'),
    ('spl', 'Spell Like'),
)

SCHOOLS_OF_MAGIC = (
    ("abj", "Abjuration"),
    ("Conjuration",
        ('creat', 'Creation),
        ('heal', 'Healing'),
        ('sum', 'Summoning'),
     ),
    ("div", "Divination"),
    ("Enchantment"
        ('charm', 'Charm'),
        ('comp', 'Compulsion'),
     ),
    ("evo", "Evocation"),
    ("Illusion"
        ('fig','Figment'),
        ('glam','Glamor'),
        ('pat','Pattern'),
        ('phant','Phantasm'),
        ('shdw','Shadow'),
    ),
    ("necro", "Necromancy"),
    ("trans", "Transmutation"),
    ("uni", "Universal"),
)

__all__ = [
    AURA_STRENGTHS,
    SCHOOLS_OF_MAGIC,
]

