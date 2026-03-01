# -*- coding: utf-8 -*-
import random
from threading import Thread, Lock

import pytest
from django.core.cache import cache

from cache_memoize import cache_memoize

from .dummy_package import a as dummy_a
from .dummy_package import b as dummy_b


def test_the_setup():
    """If this doesn't work, the settings' CACHES isn't working."""
    cache.set("foo", "bar", 1)
    assert cache.get("foo") == "bar"


def test_cache_memoize():
    calls_made = []

    @cache_memoize(10)
    def runmeonce(a, b, k1="bla", k2=None):
        calls_made.append((a, b, k1, k2))
        return "{} {} {} {}".format(a, b, k1, k2)  # sample implementation

    runmeonce(1, 2)
    runmeonce(1, 2)
    assert len(calls_made) == 1
    runmeonce(1, 3)
    assert len(calls_made) == 2
    # Should work with most basic types
    runmeonce(1.1, "foo")
    runmeonce(1.1, "foo")
    assert len(calls_made) == 3
    # Even more "advanced" types
    runmeonce(1.1, "foo", k1=list("åäö"))
    runmeonce(1.1, "foo", k1=list("åäö"))
    assert len(calls_made) == 4
    # And shouldn't be a problem even if the arguments are really long
    runmeonce("A" * 200, "B" * 200, {"C" * 100: "D" * 100})
    assert len(calls_made) == 5
    # The order of the keyword arguments doesn't matter
    runmeonce(1, 2, k1=3, k2=4)
    runmeonce(1, 2, k2=4, k1=3)
    assert len(calls_made) == 6


@pytest.mark.parametrize(
    ("obj_1", "obj_2"),
    [
        # Check identically named entities from different modules
        (dummy_a.func, dummy_b.func),
        (dummy_a.decorated_func, dummy_b.decorated_func),
        (dummy_a.DummyClass().func, dummy_b.DummyClass().func),
        (dummy_a.DummyClass().decorated_func, dummy_b.DummyClass().decorated_func),
        #
        # Check identically named entities from different scopes
        (dummy_a.func, dummy_a.DummyClass().func),
        (dummy_a.func, dummy_a.func_factory()),
        #
        # Check decorated entities
        (dummy_a.decorated_func, dummy_a.another_decorated_func),
        (
            dummy_a.DummyClass().decorated_func,
            dummy_a.DummyClass().another_decorated_func,
        ),
    ],
)
def test_default_prefix_uniqueness(obj_1, obj_2):
    assert obj_1.get_cache_key() != obj_2.get_cache_key()


def test_prefixes():
    calls_made = []

    # different prefixes
    @cache_memoize(10, prefix="first")
    def foo(value):
        calls_made.append(value)
        return "ho"

    @cache_memoize(10, prefix="second")
    def bar(value):
        calls_made.append(value)
        return "ho"

    foo("hey")
    assert len(calls_made) == 1
    bar("hey")
    assert len(calls_made) == 2


def test_no_store_result():
    calls_made = []

    # Test when you don't care about the result
    @cache_memoize(10, store_result=False, prefix="different")
    def returnnothing(a, b, k="bla"):
        calls_made.append((a, b, k))
        # note it returns None

    returnnothing(1, 2)
    returnnothing(1, 2)
    assert len(calls_made) == 1


class TestDefaultCacheKeyQuoting:
    @pytest.mark.parametrize(
        "bits", [("a", "b", "c"), ("ä", "á", "ö"), ("ë".encode(), b"\02", b"i")]
    )
    def test_colons_quoting(self, bits):
        calls_made = []

        @cache_memoize(10)
        def fun(a, b, k="bla"):
            calls_made.append((a, b, k))
            return (a, b, k)

        sep = ":"
        if isinstance(bits[0], bytes):
            sep = sep.encode()
        a1, a2 = (sep.join(bits[:2]), bits[2])
        b1, b2 = (bits[0], sep.join(bits[1:]))
        fun(a1, a2)
        fun(b1, b2)
        assert len(calls_made) == 2

    @pytest.mark.parametrize(
        ("arguments_1", "arguments_2"),
        [
            (
                (("a", "b", "c"), {}),
                (("a:b:c",), {}),
            ),
            (
                (("a", "b"), {"c": "d"}),
                (("a",), {"b:c": "d"}),
            ),
            (
                (("a",), {"b": "c"}),
                (("a", "b=c"), {}),
            ),
            (
                ((), {"a": "b=c"}),
                ((), {"a=b": "c"}),
            ),
        ],
    )
    def test_general_quoting(self, arguments_1, arguments_2):
        calls_made = []

        @cache_memoize(10)
        def fun(*args, **kwargs):
            calls_made.append((args, kwargs))

        args, kwargs = arguments_1
        fun(*args, **kwargs)

        args, kwargs = arguments_2
        fun(*args, **kwargs)

        assert calls_made == [arguments_1, arguments_2]


def test_cache_memoize_hit_miss_callables():
    hits = []
    misses = []
    calls_made = []

    def hit_callable(arg):
        hits.append(arg)

    def miss_callable(arg):
        misses.append(arg)

    @cache_memoize(10, hit_callable=hit_callable, miss_callable=miss_callable)
    def runmeonce(arg):
        calls_made.append(arg)
        return arg * 2

    result = runmeonce(100)
    assert result == 200
    assert len(calls_made) == 1
    assert len(hits) == 0
    assert len(misses) == 1

    result = runmeonce(100)
    assert result == 200
    assert len(calls_made) == 1
    assert len(hits) == 1
    assert len(misses) == 1

    result = runmeonce(100)
    assert result == 200
    assert len(calls_made) == 1
    assert len(hits) == 2
    assert len(misses) == 1

    result = runmeonce(200)
    assert result == 400
    assert len(calls_made) == 2
    assert len(hits) == 2
    assert len(misses) == 2


def test_cache_memoize_refresh():
    calls_made = []

    @cache_memoize(10)
    def runmeonce(a):
        calls_made.append(a)
        return a * 2

    runmeonce(10)
    assert len(calls_made) == 1
    runmeonce(10)
    assert len(calls_made) == 1
    runmeonce(10, _refresh=True)
    assert len(calls_made) == 2


def test_cache_memoize_different_functions_same_arguments():
    calls_made_1 = []
    calls_made_2 = []

    @cache_memoize(10)
    def function_1(a):
        calls_made_1.append(a)
        return a * 2

    @cache_memoize(10)
    def function_2(a):
        calls_made_2.append(a)
        return a * 3

    assert function_1(100) == 200
    assert len(calls_made_1) == 1

    assert function_1(100) == 200
    assert len(calls_made_1) == 1

    # Same arguments but to different function
    assert function_2(100) == 300
    assert len(calls_made_1) == 1
    assert len(calls_made_2) == 1

    assert function_2(100) == 300
    assert len(calls_made_1) == 1
    assert len(calls_made_2) == 1

    assert function_2(1000) == 3000
    assert len(calls_made_1) == 1
    assert len(calls_made_2) == 2

    # If you set the prefix, you can cross wire functions.
    # Note sure why you'd ever want to do this though

    @cache_memoize(
        10, prefix=".".join((function_2.__module__, function_2.__qualname__))
    )
    def function_3(a):
        raise Exception

    assert function_3(100) == 300


def test_invalidate():
    calls_made = []

    @cache_memoize(10)
    def function(argument):
        calls_made.append(argument)
        return random.random()

    value = function(100)
    assert value == function(100)
    assert len(calls_made) == 1
    function.invalidate(999)  # different args
    assert value == function(100)
    assert len(calls_made) == 1
    function.invalidate(100)  # known args
    assert value != function(100)
    assert len(calls_made) == 2


def test_invalidate_with_refresh():
    calls_made = []

    @cache_memoize(10)
    def function(argument):
        calls_made.append(argument)
        return random.random()

    value = function(100, _refresh=False)
    assert value == function(100, _refresh=False)
    assert len(calls_made) == 1
    new_value = function(100, _refresh=True)
    assert value != new_value
    assert len(calls_made) == 2

    function.invalidate(999, _refresh=True)  # different args
    assert new_value == function(100, _refresh=False)
    assert len(calls_made) == 2
    function.invalidate(100, _refresh=0)  # known args
    assert new_value != function(100, _refresh=False)
    assert len(calls_made) == 3


def test_get_cache_key():
    @cache_memoize(10)
    def funky(argument):
        pass

    assert funky.get_cache_key(100) == "eb96668ba0d14dc7748161fb1d000239"
    assert funky.get_cache_key(100, _refresh=True) == "eb96668ba0d14dc7748161fb1d000239"


def test_cache_memoize_custom_alias():
    calls_made = []

    def runmeonce(a):
        calls_made.append(a)
        return a * 2

    runmeonce_default = cache_memoize(10)(runmeonce)
    runmeonce_locmem = cache_memoize(10, cache_alias="other")(runmeonce)

    runmeonce_default(10)
    assert len(calls_made) == 1
    runmeonce_default(10)
    assert len(calls_made) == 1
    runmeonce_locmem(10)
    assert len(calls_made) == 2
    runmeonce_locmem(10)
    assert len(calls_made) == 2


def test_cache_memoize_works_with_custom_key_generator():
    calls_made = []

    def key_generator(*args):
        key = (":{}" * len(args)).format(*args)
        return "custom_namespace:{}".format(key)

    @cache_memoize(10, key_generator_callable=key_generator)
    def runmeonce(arg1, arg2):
        calls_made.append((arg1, arg2))
        return arg1 + 1

    runmeonce(1, 2)
    runmeonce(1, 2)
    assert len(calls_made) == 1
    runmeonce(1, 3)
    assert len(calls_made) == 2


def test_invalidate_with_custom_key_generator():
    calls_made = []

    def key_generator(*args):
        key = (":{}" * len(args)).format(*args)
        return "custom_namespace:{}".format(key)

    @cache_memoize(10, key_generator_callable=key_generator)
    def runmeonce(arg1, arg2):
        calls_made.append((arg1, arg2))
        return arg1 + 1

    runmeonce(1, 2)
    runmeonce(1, 2)
    assert len(calls_made) == 1
    runmeonce.invalidate(999, 10)  # different args
    assert runmeonce(1, 2)
    assert len(calls_made) == 1

    runmeonce.invalidate(1, 2)  # known args
    assert runmeonce(1, 2)
    assert len(calls_made) == 2


def test_get_cache_key_with_custom_key_generator():
    @cache_memoize(10, key_generator_callable=lambda x: x * 10)
    def funky(argument):
        pass

    assert funky.get_cache_key("1") == "1111111111"


def test_get_cache_key_with_extra_components():
    def funky(argument):
        pass

    fn1 = cache_memoize(10, extra={"version": 1})(funky)
    fn2 = cache_memoize(10, extra={"version": 1})(funky)
    fn3 = cache_memoize(10, extra={"version": 2})(funky)
    fn4 = cache_memoize(10, extra=lambda x: x * 2)(funky)
    fn5 = cache_memoize(10, extra=lambda x: x * 3)(funky)

    assert fn1.get_cache_key(1) == fn2.get_cache_key(1)
    assert fn2.get_cache_key(1) != fn3.get_cache_key(1)
    assert fn4.get_cache_key(1) != fn5.get_cache_key(1)


def test_cache_memoize_none_value():
    calls_made = []

    @cache_memoize(10)
    def runmeonce(a):
        calls_made.append(a)

    result = runmeonce(20)
    assert len(calls_made) == 1
    assert result is None
    result = runmeonce(20)
    assert len(calls_made) == 1
    assert result is None


def test_cache_memoize_thread_safety():
    calls_made = []

    lock = Lock()

    @cache_memoize(10, cache_alias="thread_local", args_rewrite=lambda *args: args[1:])
    def runmeonce(_calls_made, a):
        # Do not include _calls_made in the key.
        # Because we're using threads, call_made cannot be used from the
        # outer scope, so we need to inject it with the arguments.
        with lock:
            return _calls_made.append(a)

    def func_that_calls_runmeonce(*args):
        runmeonce(*args)

    threads = [
        Thread(target=func_that_calls_runmeonce, args=(calls_made, 1)) for x in range(2)
    ]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert len(calls_made) == 2


class TestException(Exception):
    pass


class DerivedTestException(TestException):
    pass


class SecondTestException(Exception):
    pass


def test_dont_cache_exceptions():
    calls_made = []

    @cache_memoize(10, prefix="dont_cache_exceptions")
    def raise_test_exception():
        calls_made.append(1)
        raise TestException

    # Caching of exceptions i turned off. These should both call the function
    # and propagate the exception.
    with pytest.raises(TestException):
        raise_test_exception()
    with pytest.raises(TestException):
        raise_test_exception()
    assert len(calls_made) == 2


def test_cache_exception():
    calls_made = []

    @cache_memoize(10, cache_exceptions=TestException, prefix="cache_exceptions")
    def raise_test_exception():
        calls_made.append(1)
        raise TestException

    # The first call should be cached, raised and the second call should
    # re-raise the cached exception without calling the cached function.
    with pytest.raises(TestException):
        raise_test_exception()
    with pytest.raises(TestException):
        raise_test_exception()
    assert len(calls_made) == 1


def test_cache_exceptions():
    calls_made = []

    # It should be possible to specify a tuple of exceptions to cache.
    @cache_memoize(
        10,
        cache_exceptions=(TestException, SecondTestException),
        prefix="cache_exceptions",
    )
    def raise_test_exception():
        calls_made.append(1)
        raise TestException

    with pytest.raises(TestException):
        raise_test_exception()
    with pytest.raises(TestException):
        raise_test_exception()
    assert len(calls_made) == 1


def test_cache_derived_exceptions():
    calls_made = []

    @cache_memoize(10, cache_exceptions=TestException, prefix="cache_exceptions")
    def raise_test_exception():
        calls_made.append(1)
        raise DerivedTestException

    # We're raising DerivedTestException, which is a subclass of TestException
    # and should thus be cached.
    with pytest.raises(DerivedTestException):
        raise_test_exception()
    with pytest.raises(DerivedTestException):
        raise_test_exception()
    assert len(calls_made) == 1


def test_dont_cache_unrelated_exceptions():
    calls_made = []

    @cache_memoize(10, cache_exceptions=TestException, prefix="cache_exceptions")
    def raise_test_exception():
        calls_made.append(1)
        raise SecondTestException

    # We're raising SecondTestException, which is not a subclass
    # of TestException, so the calls shouldn't be cached.
    with pytest.raises(SecondTestException):
        raise_test_exception()
    with pytest.raises(SecondTestException):
        raise_test_exception()
    assert len(calls_made) == 2
