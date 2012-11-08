from django.db import models
from django import forms
from django.core.exceptions import ValidationError

from webdnd.shared.views import render_to_string
from webdnd.player.models.alignments import Alignment
import re


class AlignmentWidget(forms.Widget):

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


class AlignmentFormField(forms.ModelChoiceField):
    widget = AlignmentWidget


class AlignmentField(models.OneToOneField):
    __metaclass__ = models.SubfieldBase
    description = 'Stores a D&D style alignment'

    def __init__(self, *args, **kwargs):
        args = ('Alignment',)
        defaults = {
            'related_name': 'owner',
            'blank': False,
            'null': False,
        }

        defaults.update(kwargs)
        super(AlignmentField, self).__init__(*args, **defaults)

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': AlignmentFormField}
        defaults.update(kwargs)

        return super(AlignmentField, self).formfield(**defaults)


class ColorWidget(forms.Widget):

    class Media:
        css = {
            'all': ('css/spectrum.css',)
        }
        js = ('js/jquery.js', 'js/jquery-spectrum.js',)

    def render(self, name, value, attrs=None):
        return render_to_string('color_widget.html', {
            'color': value,
            'name': name,
        })

    def value_from_datadict(self, data, files, name):
        return data.get(name, None)[1:]


class ColorFormField(forms.CharField):
    widget = ColorWidget


# Any 3 or 6 digit hex code
COLOR_RE = re.compile(r'#?(?P<hex>[A-Fa-f0-9]{6})')


class ColorField(models.Field):
    __metaclass__ = models.SubfieldBase
    description = 'Stores a 6 digit hex color'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6

        super(ColorField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value == '' or value is None:
            return ''

        match = COLOR_RE.match(str(value))
        if not match:
            raise ValidationError(self.error_messages['invalid'])
        return match.group('hex')

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': ColorFormField}
        defaults.update(kwargs)

        return super(ColorField, self).formfield(**defaults)




