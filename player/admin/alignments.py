from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.forms import Widget

from webdnd.shared.views import render_to_string
from webdnd.player.models.alignments import Alignment


class AlignmentMoralListFilter(SimpleListFilter):
    title = _('alignment (Moral)')
    parameter_name = 'align_moral'

    def lookups(self, request, model_admin):
        return (
            ('good', _('Good')),
            ('neut', _('Neutral')),
            ('evil', _('Evil')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'good':
            return queryset.filter(alignment__align_moral__gte=70)
        elif self.value() == 'evil':
            return queryset.filter(alignment__align_moral__lte=30)
        elif self.value() == 'neut':
            return queryset.filter(
                alignment__align_moral__gt=30,
                alignment__align_moral__lt=70
            )


class AlignmentOrderListFilter(SimpleListFilter):
    title = _('alignment (Order)')
    parameter_name = 'align_order'

    def lookups(self, request, model_admin):
        return (
            ('law', _('Lawful')),
            ('neut', _('Neutral')),
            ('chaos', _('Chaotic')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'law':
            return queryset.filter(alignment__align_order__gte=70)
        elif self.value() == 'chaos':
            return queryset.filter(alignment__align_order__lte=30)
        elif self.value() == 'neut':
            return queryset.filter(
                alignment__align_order__gt=30,
                alignment__align_order__lt=70
            )



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
        });

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

