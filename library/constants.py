STND_CHAR_LIMIT = 100
STND_ID_CHAR_LIMIT = 5

STND_MASS_UNIT = 'kg'
STND_VOLUME_UNIT = 'L'
STND_LENGTH_UNIT = 'm'
STND_THICKNESS_UNIT = 'in'
STND_TIME_UNIT = 'sec'

REFERENCE_KINDS = (
    ('home', 'homebrew'),
    ('book', 'book'),
    ('mag', 'magazine'),
    # TODO: add other types
)

SKILL_SAMPLE_TYPES = (
    ('dc', 'DC'),
    ('mod', 'modifier'),
)

ACTION_TYPES = (
    ('free', 'Free'),
    ('part', 'Partial'),
    ('stnd', 'Standard'),
    ('movt', 'Movement'),
    ('imdt', 'Immediate'),
    ('swft', 'Swift'),
    ('full', 'Full Round'),
)

ARMOR_TYPES = (
   ('l', 'Light'),
   ('m', 'Medium'),
   ('h', 'Heavy'),
   ('s', 'Shield'),
)

ATTRIBUTES = (
	('str', 'Strength'),
	('con', 'Constitution'),
	('dex', 'Dexterity'),
	('int', 'Intelligence'),
	('wis', 'Wisdom'),
	('cha', 'Charisma'),
)

AURA_STRENGTHS = (
   ('dim', 'Dim'),
   ('fnt', 'Faint'),
   ('mod', 'Moderate'),
   ('strng', 'Strong'),
   ('op', 'Overpowering'),
)

DAMAGE_TYPES = (
   ('b', 'Bludgeoning'),
   ('s', 'Slashing'),
   ('p', 'Piercing'),
)

GEM_QUALITIES = (
    ('chip', 'Chipped'),
    ('fine', 'Fine'),
    ('flwls', 'Flawless'),
    ('prfct', 'Perfect'),
)

MAGIC_ITEM_SLOTS = (
   ('head', 'Head'),
   ('eyes', 'Eyes'),
   ('neck', 'Neck'),
   ('torso', 'Torso'),
   ('body', 'Body'),
   ('wst', 'Waist'),
   ('shldr', 'Shoulders'),
   ('arms', 'Arms'),
   ('glvs', 'Gloves'),
   ('ring', 'Ring'), # x2
   ('feet', 'Feet'),
   ('misc', 'Miscellaneous'), # any amount
   ('enhc', 'Enhancement')
)

MAGIC_ITEM_STRENGTHS = (
   ('minor', 'Minor'),
   ('mdium', 'Medium'),
   ('major', 'Major'),
   ('mnart', 'Minor Artifact'),
   ('mjart', 'Major Artifact'),
)

POISON_TYPES = (
	('cntct', 'Contact'),
	('ingst', 'Ingested'),
	('inhl', 'Inhaled'),
	('injr', 'Injury'),
)

SAVING_THROWS = (
   ('fort', 'Fortitude'),
   ('ref', 'Reflex'),
   ('will', 'Will'),
)

SCHOOLS_OF_MAGIC = (
   ('abj', 'Abjuration'),
   ('conj', 'Conjuration'),
   ('div', 'Divination'),
   ('ench', 'Enchantment'),
   ('evo', 'Evocation'),
   ('illu', 'Illusion'),
   ('necro', 'Necromancy'),
   ('trans', 'Transmutation'),
   ('uni', 'Universal'),
)

SIZES = (
    ('f', 'Fine'),
    ('d', 'Diminuitive'),
    ('t', 'Tiny'),
    ('s', 'Small'),
    ('m', 'Medium'),
    ('l', 'Large'),
    ('h', 'Huge'),
    ('g', 'Gargantuan'),
    ('c', 'Colossal'),
)

WEAPON_TYPES = (
    ('bow', 'Bow'),
    ('xbow', 'Crossbow'),
    ('thrw', 'Thrown'),
    ('slng', 'Sling'),
    ('swrd', 'Sword'),
    ('axe', 'Axe'),
    ('mace', 'Mace'),
    ('plrm', 'Polearm'),
)

WEAPON_CLASSES = (
    ('light', 'Light'),
    ('hlfhd', 'Half-handed'),
    ('twohd', 'Two-handed'),
    ('onehd', 'One-handed'),
)

# measuring units

MASS_MEASURING_UNITS = (
	('mg', 'Milligrams'),
    ('g', 'Grams'),
    ('kg', 'Kilograms'),
	('t', 'Tonnes'),
	('lb', 'Pounds'),
	('oz', 'Ounces'),
)

TRADING_MEASURING_UNITS = (
	('mass', STND_MASS_UNIT), 
	('item', 'Item'), 
	('use', 'Use'),
	('vol', STND_VOLUME_UNIT),
    ('cntnr', 'Container'),
    ('len', STND_LENGTH_UNIT)
)

VOLUME_MEASURING_UNITS = (
    ('mL', 'Millilitres'),
    ('L', 'Litres'),
    ('fl oz', 'Fluid ounzes'),
    ('cu ft', 'Cubic feet'),
    ('m cu', 'Cubic metres'),
    ('pints', 'Pints'),
    ('qt', 'Quarts'),
)

LENGTH_MEASURING_UNITS = (
	('ft', 'Feet'),
	('in', 'Inches'),
	('yd', 'Yards'),
	('m', 'Metres'),
    ('mm', 'Millimetres'),
    ('cm', 'Centimetres'),
    ('mi', 'Miles'),
    ('km', 'Kilometres'),
)

TIME_MEASURING_UNITS = (
    ('sec', 'Seconds'),
    ('min', 'Minutes'),
    ('hr', 'Hours'),
    ('day', 'Days'),
    ('rnd', 'Round'),
)
