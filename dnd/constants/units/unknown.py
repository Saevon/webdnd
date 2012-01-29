ACTION_TYPES = (
    ("free", "Free"),
    ("part", "Partial"),
    ("stnd", "Standard"),
    ("movt", "Movement"),
    ("imdt", "Immediate"),
    ("swft", "Swift"),
    ("full", "Full Round"),
)

# measuring units

MASS_MEASURING_UNITS = (
    ("mg", "Milligrams"),
    ("g", "Grams"),
    ("kg", "Kilograms"),
    ("t", "Tonnes"),
    ("lb", "Pounds"),
    ("oz", "Ounces"),
)

LENGTH_MEASURING_UNITS = (
    ("ft", "Feet"),
    ("in", "Inches"),
    ("yd", "Yards"),
    ("m", "Metres"),
    ("mm", "Millimetres"),
    ("cm", "Centimetres"),
    ("mi", "Miles"),
    ("km", "Kilometres"),
)

TIME_MEASURING_UNITS = (
    ("sec", "Seconds"),
    ("min", "Minutes"),
    ("hr", "Hours"),
    ("day", "Days"),
    ("rnd", "Round"),
)

TRADING_MEASURING_UNITS = (
    ("mass", STND_MASS_UNIT), 
    ("item", "Item"), 
    ("use", "Use"),
    ("vol", STND_VOLUME_UNIT),
    ("cntnr", "Container"),
    ("len", STND_LENGTH_UNIT)
)

VOLUME_MEASURING_UNITS = (
    ("mL", "Millilitres"),
    ("L", "Litres"),
    ("fl oz", "Fluid ounzes"),
    ("cu ft", "Cubic feet"),
    ("m cu", "Cubic metres"),
    ("pints", "Pints"),
    ("qt", "Quarts"),
)
