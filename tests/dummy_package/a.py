from cache_memoize import cache_memoize

from . import dummy_decorator


@cache_memoize(None)
def func():
    pass


@cache_memoize(None)
@dummy_decorator()
def decorated_func():
    pass


@cache_memoize(None)
def another_decorated_func():
    pass


def func_factory():
    @cache_memoize(None)
    def func():
        pass

    return func


class DummyClass:
    @cache_memoize(None)
    def func(self):
        pass

    @cache_memoize(None)
    @dummy_decorator()
    def decorated_func(self):
        pass

    @cache_memoize(None)
    @dummy_decorator()
    def another_decorated_func(self):
        pass
