from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter


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
