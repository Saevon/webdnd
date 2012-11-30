from django.utils import unittest
from django.http import HttpResponse

from webdnd.shared.utils.decorators import (
    cascade,
    dirty_cache,
    cache, CacheDirty, CacheUnused,
    json_return,
)


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

    @cache
    def get_c_counter(self, bonus, other=0):
        return self.counter + bonus + other

    def _get_c_counter_cache_key(self, bonus, other=0):
        key = '%s-%s' % (self.counter, bonus)

        if other >= 100:
            raise CacheUnused
        elif other <= -100:
            raise CacheDirty(key)

        return key

    @json_return
    def get_jr_counter(self, http=False):
        if http:
            self.response = HttpResponse()
            return self.response
        else:
            return {'count': self.counter}



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



class TestCache(unittest.TestCase):

    def setUp(self):
        self.foo = Foo()

    def test_one_use(self):
        self.assertEqual(self.foo.get_c_counter(0, 0), 0)

    def test_caching(self):
        self.foo.count(2)

        # Second arg isn't part of the key
        self.assertEqual(self.foo.get_c_counter(0, 1), 3)
        self.assertEqual(self.foo.get_c_counter(0, 2), 3)

        # Changing self should only affect the cache if its part of the key
        self.foo.other = 12
        self.assertEqual(self.foo.get_c_counter(0, 1), 3)
        self.foo.count(2)
        self.assertEqual(self.foo.get_c_counter(0, 1), 5)

        # Try and get other cached data
        self.assertEqual(self.foo.get_c_counter(1, 10), 15)
        self.assertEqual(self.foo.get_c_counter(2, 15), 21)
        self.assertEqual(self.foo.get_c_counter(1, 0), 15)


    def test_caching__reset_arg(self):
        self.foo.count(2)

        self.assertEqual(self.foo.get_c_counter(0), 2)
        self.assertEqual(self.foo.get_c_counter(1, _reset_cache=True), 3)
        self.foo.count(2)
        self.assertEqual(self.foo.get_c_counter(0, _reset_cache=True), 4)
        self.assertEqual(self.foo.get_c_counter(1, _reset_cache=True), 5)

    def test_caching__cache_key_unused_cache(self):
        self.foo.count(2)

        self.assertEqual(self.foo.get_c_counter(1, 0), 3)
        self.assertEqual(self.foo.get_c_counter(1, 12), 3)
        self.assertEqual(self.foo.get_c_counter(1, 100), 103)
        # Should still contain the older value
        self.assertEqual(self.foo.get_c_counter(1, 0), 3)

    def test_caching__cache_key_dirty_cache(self):
        self.foo.count(2)

        self.assertEqual(self.foo.get_c_counter(1, 0), 3)
        self.assertEqual(self.foo.get_c_counter(1, 12), 3)
        self.assertEqual(self.foo.get_c_counter(1, -100), -97)
        self.assertEqual(self.foo.get_c_counter(1, 0), -97)



class TestJsonReturn(unittest.TestCase):

    def setUp(self):
        self.foo = Foo()

    def test_data(self):
        response = self.foo.get_jr_counter()

        self.assertEqual(response.content, '{"count": 0}')

    def test_http_response(self):
        response = self.foo.get_jr_counter(http=True)
        self.assertIs(response, self.foo.response)




