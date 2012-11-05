

def fk_link(field):
    '''
    Used in fields or fieldsets, turns the field into a link to the object
    '''
    def link(obj):
        attr = getattr(obj, field)
        url = '/admin/%s/%s/%d' % (
            attr._meta.app_label,
            attr._meta.module_name,
            attr.id
        )

        return '<a href="%s">%s</a>' % (url, attr)

    link.__name__ = field
    link.allow_tags = True
    return link
