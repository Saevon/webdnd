from collections import defaultdict
from itertools import chain
from webdnd.shared.utils.decorators import cascade, dirty_cache


class StatVal(dict):
    '''
    An int with some stats about it
    '''

    def __init__(self, value, stats=None):
        super(StatVal, self).__init__(stats or {})
        self['value'] = value



class ModField(object):

    def __init__(self, value):
        super(ModField, self).__init__()
        self._label = ''
        self._kind = ''

        obj = self.StatVal(value, {'change_type': 'start'})
        self._hist = [obj]
        self._value = obj

    def __repr__(self):
        return '%s' % (unicode(self))

    def __unicode__(self):
        return u'"%s"' % self.get()

    def StatVal(self, value='', stats=None):
        '''
        Returns a new personalized StatVal
        '''
        defaults = {
            'label': self._label,
            'kind': self._kind,
        }
        defaults.update(stats or {})
        return StatVal(value, defaults)

    @cascade
    def set(self, value):
        '''
        Changes the value of this field
        '''
        self._get_dirty = True

        val = self.StatVal(value)
        val['change_type'] = 'set'

        self._value = val
        self._hist.append(val)

    def get(self):
        '''
        Returns the value of this field
        '''
        return self._value['value']

    @cascade
    def set_label(self, label, kind):
        '''
        Sets the label applied to changes made by this field
        '''
        self._label = label
        self._kind = kind

    def result(self):
        '''
        Returns the final result of this field
        '''
        return {
            'value': self.get(),
            'history': self._hist
        }


class FilteredModField(ModField):

    def __init__(self, value, filter):
        super(FilteredModField, self).__init__(value)
        self._filter = filter

    def set(self, value):
        if not self._filter(value):
            return False
        else:
            return super(FilteredModField, self).set(value)


class ReadOnlyModField(ModField):

    def __init__(self, value):
        super(ReadOnlyModField, self).__init__(value)
        self._orig = value

    def set(self, *args, **kwargs):
        return False

    def get(self):
        return self._orig

    def result(self):
        '''
        Returns the final result of this field
        '''
        raise LookupError("Can't get the value of a Read-Only Field, Use the original value.")


class NumModField(ModField):

    def __init__(self, value):
        value = int(value)
        super(NumModField, self).__init__(value)

        self._penalties = defaultdict(lambda: self.StatVal())
        self._bonuses = defaultdict(lambda: self.StatVal())
        self._unnamed_changes = []

        self._mult = []
        self._mult_val = 1

    def __unicode__(self):
        return u'%s' % (self.get())

    def StatVal(self, value=0, stats=None):
        return super(NumModField, self).StatVal(value, stats)

    @cascade
    def add(self, value, name=None):
        '''
        Adds a bonus with an optional name to the field
        '''
        self._get_dirty = True
        obj = self.StatVal(value)

        # Negative bonuses are penalties
        if value < 0:
            obj['value'] = -1 * value
            obj['is_bonus'] = False
            kind = self._penalties
        else:
            obj['is_bonus'] = True
            kind = self._bonuses

        if name is None:
            obj['name'] = None
            self._unnamed_changes.append(obj)
        else:
            obj['name'] = name
            kind[name] = obj

        obj['change_type'] = 'add/sub'
        self._hist.append(obj)

    @cascade
    def sub(self, value, name=None):
        '''
        Adds a penalty with an optional name to the field
        '''
        self.add(-1 * value, name)

    @cascade
    def mul(self, value):
        '''
        Adds a D&D style multiplier to the field
        '''
        self._get_dirty = True
        obj = self.StatVal(value)

        self._mult.append(obj)
        self._mult_val += value - 1

        obj['change_type'] = 'mul'
        self._hist.append(obj)

    @dirty_cache
    def get(self):
        '''
        Returns the current value of the field
        '''
        val = super(NumModField, self).get()

        for change in chain(self._bonuses.values(), self._unnamed_changes, self._penalties.values()):
            val += change['value'] * (1 if change['is_bonus'] else -1)

        val *= self._mult_val
        return val


class DmgModField(NumModField):

    DEFAULT_DMG = 'physical'

    def __init__(self, value):
        super(DmgModField, self).__init__(value)

    @cascade
    def add(self, value, name=None, dmg_type=None):
        '''
        Applies a bonus to damage
        '''
        self._get_dirty = True
        obj = self.StatVal(value)

        dmg_type = DmgModField.DEFAULT_DMG if dmg_type is None else dmg_type
        obj['dmg_type'] = dmg_type

        # Negative bonuses are penalties
        if value < 0:
            obj['value'] = -1 * value
            obj['is_bonus'] = False
            kind = self._penalties
        else:
            obj['is_bonus'] = True
            kind = self._bonuses

        if name is None:
            obj['name'] = None
            self._unnamed_changes.append(obj)
        else:
            obj['name'] = name
            kind[name] = obj

        obj['change_type'] = 'add/sub'
        self._hist.append(obj)

    @cascade
    def sub(self, value, name=None, dmg_type=None):
        '''
        Applies a penalty to damage
        '''
        self.add(-1 * value, name, dmg_type)


class StatModField(NumModField):

    def __init__(self, value, disabled=False):
        super(StatModField, self).__init__(value)
        if disabled:
            self.disable()
        else:
            self.__disabled = False

    def __unicode__(self):
        val = self.get()
        if val:
            return '%s (%s)' % (val, self.mod())
        else:
            return 'Disabled'

    def get(self):
        '''
        Returns the current stat value
            Returns False if the stat is disabled
        '''
        if self.__disabled:
            return False
        return super(StatModField, self).get()

    def mod(self):
        '''
        Returns the modifier for the stat
        '''
        val = self.get()
        if val is False:
            return 0
        return (val - (val % 2) - 10) / 2

    @cascade
    def disable(self):
        '''
        Disables the stat, setting the stat after this will have no visible effects
        '''
        # TODO: side effects? e.g. no CON means you fail all fort saves
        obj = self.StatVal(True)
        obj['change_type'] = 'enable/disable'
        self._hist.append(obj)

        self.__disabled = True

    @cascade
    def enable(self):
        '''
        Enables the stat
        '''
        obj = self.StatVal(False)
        obj['change_type'] = 'enable/disable'
        self._hist.append(obj)

        self.__disabled = False

    def is_enabled(self):
        '''
        Returns True if this stat is enabled
        '''
        return not self.__disabled

    def result(self):
        '''
        Returns the final result of this field
        '''
        result = super(StatModField, self).result()
        result.update({
            'enabled': self.is_enabled(),
            'modifier': self.mod(),
        })
        return result

