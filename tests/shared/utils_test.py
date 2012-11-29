from django.utils import unittest

from webdnd.shared.utils.decorators import dirty_cache, cascade


class Foo(object):
    """Class to test decorators"""
    def __init__(self):
        self.counter = 0

    @cascade
    def set_val(self, val):
        self.counter = val

    @cascade
    def count(self, val):
        self.counter = self.counter + val

    def get_count(self):
        return self.counter

    @dirty_cache
    def get_dc_counter(self, bonus):
        return self.counter + bonus

class TestCascade(unittest.TestCase):

    def setUp(self):
        self.foo = Foo()

    def test_basic(self):
        out = (self.foo.set_val(3)
            .count(4)
            .count(5)
        )

        self.assertEqual(out, self.foo)
        self.assertEqual(out.get_count(), 12)


class TestDirtyCache(unittest.TestCase):

    def setUp(self):
        self.foo = Foo()

    def test_one_use(self):
        self.assertEqual(self.foo.get_dc_counter(0), 0)

    def test_caching__by_args(self):
        self.foo.count(2)
        
        self.assertEqual(self.foo.get_dc_counter(0), 2)
        self.assertEqual(self.foo.get_dc_counter(12), 2)

    def test_caching__by_attrs(self):
        self.foo.count(2)
        
        self.assertEqual(self.foo.get_dc_counter(0), 2)
        self.foo.count(2)
        self.assertEqual(self.foo.get_dc_counter(0), 2)

    def test_caching__reset_arg(self):
        self.foo.count(2)

        self.assertEqual(self.foo.get_dc_counter(0), 2)
        self.assertEqual(self.foo.get_dc_counter(1, _reset_cache=True), 3)
        self.foo.count(2)
        self.assertEqual(self.foo.get_dc_counter(0, _reset_cache=True), 4)
        self.assertEqual(self.foo.get_dc_counter(1, _reset_cache=True), 5)

    def test_caching__reset_attr(self):
        self.foo.count(2)

        self.assertEqual(self.foo.get_dc_counter(0), 2)

        self.foo.count(2)
        self.foo._get_dc_counter_dirty = True
        self.assertEqual(self.foo.get_dc_counter(0), 4)
        self.assertEqual(self.foo.get_dc_counter(1), 4)
        self.foo.count(2)
        self.assertEqual(self.foo.get_dc_counter(0), 4)



