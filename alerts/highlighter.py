from django.conf import settings


class Highlighter(list):
    """
    A simple wrapper that allows you to highlight fields
    """

    def __init__(self):
        super(Highlighter, self).__init__()

    def __call__(self, selector, level=None, text=None):
        """
        Highlights a field, returning the new field
        """
        field = {
            'selector': selector,
            'level': sanitize_level(level),
            'text': text,
        }

        self.append(field)
        return field

    def process(self):
        """
        Transforms the highlighter into a list of fields to highlight
        """
        return list(self)

def sanitize_level(lvl):
    """
    Returns a valid highlighter level
    """
    if lvl in settings.HIGHLIGHTER_LEVELS:
        return lvl
    return settings.HIGHLIGHTER_DEFAULT_LEVEL

def template_processor(request):
    """
    Adds the alerts to the template context
    """
    return {
        'highlighted_fields': request.highlight.process(),
    }
