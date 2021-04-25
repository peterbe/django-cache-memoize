from cache_memoize import cache_memoize

from . import dummy_decorator


@cache_memoize(None)
def func():
    pass


@cache_memoize(None)
@dummy_decorator()
def decorated_func():
    pass


class DummyClass:
    @cache_memoize(None)
    def func(self):
        pass

    @cache_memoize(None)
    @dummy_decorator()
    def decorated_func(self):
        pass
