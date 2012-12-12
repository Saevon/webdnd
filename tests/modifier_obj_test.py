from django.utils import unittest

from webdnd.player.modifier_obj import *


class TestStatVal(unittest.TestCase):

    def test__basic(self):
        val = StatVal(12)

        self.assertEquals(val['value'], 12)

    def test__stats(self):
        val = StatVal(12, {'a': 5})

        self.assertEquals(val['value'], 12)
        self.assertEquals(val['a'], 5)


class TestModField(unittest.TestCase):

    start = 0

    def setUp(self):
        self.field = ModField(self.start)

    @property
    def last_change(self):
        return self.change(-1)

    def change(self, value):
        return self.field.result()['history'][value]

    def test_mod__StatVal(self):
        self.assertEquals(self.field.StatVal(12, {'yay': 2})['yay'], 2)
        self.assertEquals(self.field.StatVal(12)['label'], '')
        self.assertEquals(self.field.StatVal(12)['kind'], '')

    def test_mod__basic(self):
        self.assertEquals(self.field.get(), self.start)
        self.assertEquals(self.field.result()['value'], self.start)

    def test_mod__set(self):
        new = 2
        self.field.set(new)
        self.assertEquals(self.field.get(), new)
        self.assertEquals(self.field.result()['value'], new)

    def test_mod__history__start(self):
        self.assertEquals(self.change(0)['value'], self.start)

    def test_mod__labels(self):
        self.assertEquals(self.last_change['label'], '')
        self.assertEquals(self.last_change['kind'], '')

        # The label doesn't affect the current or past values
        self.field.set_label('dodge', 'ability')
        self.assertEquals(self.last_change['label'], '')
        self.assertEquals(self.last_change['kind'], '')

        self.field.set(2)
        self.assertEquals(self.last_change['label'], 'dodge')
        self.assertEquals(self.last_change['kind'], 'ability')

    def test_mod__change_type(self):
        self.assertEquals(self.last_change['change_type'], 'start')

        self.field.set(2)
        self.assertEquals(self.last_change['change_type'], 'set')

    def test_mod__history(self):
        self.field.set(1)
        self.field.set(2)

        # start, set, set == three historical values
        self.assertEquals(len(self.field.result()['history']), 3)

        # Make sure all the values were kept properly
        self.assertEquals(self.change(1)['value'], 1)
        self.assertEquals(self.change(1)['change_type'], 'set')


class TestFilteredModField(TestModField):

    def setUp(self):
        self.field = FilteredModField(self.start, filter=lambda v: v < 100)

    def test__basic(self):
        self.assertEquals(self.field.set(1000), False)
        self.assertEquals(self.field.get(), self.start)

        self.assertNotEquals(self.field.set(12), False)
        self.assertEquals(self.field.get(), 12)


class TestReadOnlyModField(unittest.TestCase):

    def test__basic(self):
        field = ReadOnlyModField('test')

        self.assertEquals(field.set('a'), False)
        self.assertEquals(field.get(), 'test')

        with self.assertRaises(LookupError):
            field.result()


class TestNumModField(TestModField):

    start = 0

    def setUp(self):
        self.field = NumModField(self.start)

    def test__mul(self):
        self.field.mul(2)
        self.assertEquals(self.field.get(), 0)

        self.field.set(1)
        self.field.mul(2)
        self.assertEquals(self.field.get(), 3)

        self.field.mul(5)
        self.assertEquals(self.field.get(), 7)

        # The multiplier is separate from the value and is always
        # applied last, so any changes to the value will be mutliplied
        self.field.set(0)
        self.field.set(1)
        self.assertEquals(self.field.get(), 7)


    def test__mul__change_type(self):
        self.field.mul(2)

        self.assertEquals(self.last_change['change_type'], 'mul')

    def test__add(self):
        self.field.add(5)
        self.assertEquals(self.field.get(), 5)

        self.field.add(5)
        self.assertEquals(self.field.get(), 10)

    def test__sub(self):
        self.field.sub(5)
        self.assertEquals(self.field.get(), -5)

        self.field.sub(5)
        self.assertEquals(self.field.get(), -10)

    def test__add_sub(self):
        self.field.add(5)
        self.field.sub(2)
        self.assertEquals(self.field.get(), 3)

    def test__add__named(self):
        self.field.add(2)
        self.field.add(2, name='cool')
        self.field.add(3, name='cool')
        self.assertEquals(self.field.get(), 5)

    def test__sub__named(self):
        self.field.sub(5)
        self.field.sub(2, name='cool')
        self.field.sub(3, name='cool')
        self.assertEquals(self.field.get(), -8)

    def test__add__change_type(self):
        self.field.add(2)
        self.assertEquals(self.last_change['change_type'], 'add/sub')
        self.assertEquals(self.last_change['is_bonus'], True)

    def test__sub__change_type(self):
        self.field.sub(2)
        self.assertEquals(self.last_change['change_type'], 'add/sub')
        self.assertEquals(self.last_change['is_bonus'], False)

    def test__complex(self):
        self.field.mul(2)
        self.field.add(5)
        self.field.sub(5, name='cool')
        self.field.sub(2)
        self.field.mul(2)

        self.assertEquals(self.field.get(), -6)

        self.field.set(1)
        self.assertEquals(self.field.get(), -3)

        self.field.set(2)
        self.assertEquals(self.field.get(), 0)


class TestDmgModField(TestNumModField):

    def setUp(self):
        self.field = DmgModField(self.start)

    def test__dmg_default(self):
        self.field.add(12)
        self.assertEquals(self.last_change['dmg_type'], self.field.DEFAULT_DMG)

        self.field.sub(12)
        self.assertEquals(self.last_change['dmg_type'], self.field.DEFAULT_DMG)


class TestStatModField(TestNumModField):

    def setUp(self):
        self.field = StatModField(self.start)

    def test__mod(self):
        self.assertEquals(self.field.mod(), -5)

        self.field.set(10)
        self.assertEquals(self.field.mod(), 0)

        self.field.set(13)
        self.assertEquals(self.field.mod(), 1)

    def test__stat__result(self):
        self.assertTrue(self.field.result()['enabled'])
        self.assertEquals(self.field.result()['modifier'], -5)

    def test__disabling(self):
        self.assertTrue(self.field.is_enabled())
        self.assertEquals(self.field.get(), 0)

        self.field.disable()
        self.assertFalse(self.field.is_enabled())
        self.assertEquals(self.field.mod(), 0)
        self.assertFalse(self.field.get())

        self.field.enable()
        self.assertTrue(self.field.is_enabled())
        self.assertEquals(self.field.mod(), -5)
        self.assertEquals(self.field.get(), 0)

    def test__disabling__change_type(self):
        self.field.disable()
        self.assertEquals(self.last_change['change_type'], 'enable/disable')

        self.field.enable()
        self.assertEquals(self.last_change['change_type'], 'enable/disable')

    def test__disabling__history(self):
        self.field.disable()
        self.field.enable()

        self.change(-2)['value'] = False
        self.last_change['value'] = True




