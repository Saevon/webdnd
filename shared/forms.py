from django.db import models
from django import forms
from django.core.exceptions import ValidationError

from webdnd.shared.views import render_to_string
from webdnd.player.models.alignments import Alignment
import re


class AlignmentWidget(forms.Widget):

    class Media:
        css = {
            # 'all': ('css/alignment.css',)
        }
        js = ('js/jquery.js', 'js/jquery-draggable.js', 'player/js/alignment.js',)

    def __init__(self, *args, **kwargs):
        self.align = None
        super(AlignmentWidget, self).__init__(*args, **kwargs)

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

        if self.align is None:
            # See if this is an existing object, otherwise we're making it
            try:
                self.align = Alignment.objects.get(pk=pk)
            except Alignment.DoesNotExist:
                self.align = Alignment()

        # Update the object with the passed in values
        if not moral is None:
            self.align.align_moral = moral
        if not order is None:
            self.align.align_order = order

        # We need to return a pk .: we need a model...
        # But this also means on validation errors we create tons of new
        # Alignment objects...
        # WTF, there has got to be a better way of doing this
        self.align.save()
        return self.align.id


class AlignmentFormField(forms.ModelChoiceField):
    widget = AlignmentWidget


class AlignmentField(models.OneToOneField):
    __metaclass__ = models.SubfieldBase
    description = 'Stores a D&D style alignment'

    def __init__(self, *args, **kwargs):
        args = ('Alignment',)

        # Default arguments (can be overwritten)
        defaults = {
            'null': False,
        }
        defaults.update(kwargs)

        # Constant changes
        defaults.update({
            'related_name': 'owner',
            'blank': True,
        })
        super(AlignmentField, self).__init__(*args, **defaults)

    def formfield(self, **kwargs):
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


class ColorField(models.CharField):
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
        # Hack to override problems with the admin's default widget being used
        from django.contrib.admin.widgets import AdminTextInputWidget
        if kwargs.get('widget') == AdminTextInputWidget:
            kwargs.pop('widget')

        defaults = {'form_class': ColorFormField}
        defaults.update(kwargs)
        return super(ColorField, self).formfield(**defaults)




