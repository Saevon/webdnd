from contextlib import contextmanager

@contextmanager
def revert_attr(self, **new_values):
    old_values = [(key, getattr(self, key)) for key in new_values.keys()]
    for key, new_value in new_values.iteritems():
        setattr(self, key, new_value)
    try:
        yield self
    finally:
        for key, old_value in old_values.iteritems():
            setattr(self, key, old_value)
