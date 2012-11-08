from django.db import models
from django.forms import Widget
from django.core.exceptions import ValidationError

from webdnd.shared.views import render_to_string
from webdnd.player.models.alignments import Alignment
import re


class AlignmentWidget(Widget):

    class Media:
        css = {
            # 'all': ('alignment.css',)
        }
        js = ('js/jquery.js', 'js/jquery-draggable.js', 'player/js/alignment.js',)

    def render(self, name, value, attrs=None):
        try:
            align = Alignment.objects.get(pk=value)
        except Alignment.DoesNotExist:
            align = Alignment()

        return render_to_string('alignment_widget.html', {
            'align_text': Alignment.to_str(align.align_moral, align.align_order),
            'align': align,
        })

    def value_from_datadict(self, data, files, name):
        pk = data.get('alignment-id', None)
        moral = data.get('alignment-moral', None)
        order = data.get('alignment-order', None)

        # See if this is an existing object, otherwise we're making it
        try:
            align = Alignment.objects.get(pk=pk)
        except Alignment.DoesNotExist:
            align = Alignment.objects.create(align_moral=50, align_order=50)

        # Update the object with the passed in values
        if not moral is None:
            align.align_moral = moral
        if not order is None:
            align.align_order = order

        # Save this object
        align.save()

        return align.id


class AlignmentField(models.OneToOneField):

    description = 'Stores a D&D style alignment'

    widget = AlignmentWidget

    def __init__(self, *args, **kwargs):
        args = ('Alignment',)
        kwargs['related_name'] = 'owner'
        kwargs['blank'] = False
        kwargs['null'] = False

        super(AlignmentField, self).__init__(*args, **kwargs)


class ColorWidget(Widget):

    class Media:
        css = {
            'all': ('js/spectrum.css',)
        }
        js = ('js/jquery.js', 'js/jquery-spectrum.js',)

    def render(self, name, value, attrs=None):
        return render_to_string('color_widget.html', {
            'color': value,
            'name': name,
        })

    def value_from_datadict(self, data, files, name):
        return data.get(name, None)


# Any 3 or 6 digit hex code
COLOR_RE = re.compile(r'#?(?P<hex>[A-Fa-f0-9]{6})')


class ColorField(models.CharField):

    description = 'Stores a 6 digit hex color'

    widget = ColorWidget

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6

        super(ColorField, self).__init__(*args, **kwargs)

    def validate(self, value):
        if not COLOR_RE.match(value):
            raise ValidationError(self.error_messages['invalid'])

    def to_python(self, value):
        match = COLOR_RE.match(value)
        return match.group(hex)



