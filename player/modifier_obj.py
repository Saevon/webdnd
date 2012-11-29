from collections import defaultdict
from webdnd.shared.utils.decorators import dirty_cache


class ModField(object):

    def __init__(self, value):
        super(ModField, self).__init__()
        self.__label = ''
        self.__value = {
            'val': value,
            'label': self.__label
        }

    def set(self, value):
        '''
        Changes the value of this field
        '''
        self._get_cache_dirty = True
        self.__value['val'] = value
        self.__value['label'] = self.__label

    def get(self):
        '''
        Returns the value of this field
        '''
        return self.__value['val']

    # TODO so far labels are mainly unused

    def set_label(self, label):
        '''
        Sets the label applied to changes made by this field
        '''
        self.__label = label

    # TODO: the children need to update this

    def result(self):
        '''
        Returns the final result of this field
        '''
        return self.__value.copy()


class FilteredModField(ModField):

    def __init__(self, value, func):
        super(FilteredModField, self).__init__(value)
        self.__filter = func

    def set(self, value):
        if not self.__filter(value):
            return False
        else:
            return super(FilteredModField, self).set(value)


class ReadOnlyModField(ModField):

    def __init__(self, value):
        self.__orig = value

    def get(self):
        return self.__orig


class NumModField(ModField):

    def __init__(self, value):
        super(NumModField, self).__init__(value)

        self.__bonuses = defaultdict(0)
        self.__unnamed_bonuses = []

        self.__penalties = defaultdict(0)
        self.__unnamed_penalties = []

        self.__mult = 1

    def add(self, value, bonus=None):
        '''
        Adds a bonus with an optional name to the field
        '''
        self._get_cache_dirty = True
        obj = {
            'value': value
        }
        if bonus is None:
            self.__unnamed_bonuses.append(obj)
        else:
            self.__bonuses[bonus] = obj

    def sub(self, value, penalty=None):
        '''
        Adds a penalty with an optional name to the field
        '''
        self._get_cache_dirty = True
        obj = {
            'value': value
        }
        if penalty is None:
            self.__unnamed_penalties.append(obj)
        else:
            self.__penalties[penalty] = obj

    def mul(self, value):
        '''
        Adds a D&D style multiplier to the field
        '''
        self._get_cache_dirty = True
        self.__mult += value - 1

    @dirty_cache
    def get(self):
        '''
        Returns the current value of the field
        '''
        val = super(NumModField, self).get()
        for bonus in self.__bonuses.values():
            val += bonus['value']
        for bonus in self.__unnamed_bonuses:
            val += bonus['value']
        for penalty in self.__penalties.values():
            val -= penalty['value']
        for penalty in self.__unnamed_penalties:
            val -= penalty['value']

        val *= self.__mult
        return val


class DmgModField(NumModField):

    def __init__(self, value):
        super(DmgModField, self).__init__()

    def add(self, value, bonus='', dmg_type=None):
        '''
        Applies a bonus to damage
        '''
        super(DmgModField, self).add(value, bonus)
        if bonus is None:
            self.__unnamed_bonuses.append(value)
        else:
            self.__bonuses[bonus] = {'value': value}

    def sub(self, value, penalty='', dmg_type=None):
        '''
        Applies a penalty to damage
        '''
        super(DmgModField, self).add(value, penalty)
        if dmg_type is None:
            # TODO: default goes here
            self.__unnamed_penalties[-1]['dmg'] = 'Physical'
        else:
            self.__penalties[penalty]['dmg'] = dmg_type


class StatModField(NumModField):

    def __init__(self, value, disabled=False):
        super(StatModField, self).__init__(value)
        self.__disabled = disabled

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

    def disable(self):
        '''
        Disables the stat
        '''
        # TODO: side effects? e.g. no CON means you fail all fort saves
        self.__disabled = True

    def enable(self):
        '''
        Enables the stat
        '''
        self.__disabled = False


