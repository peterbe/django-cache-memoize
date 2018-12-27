import pytest


@pytest.fixture(autouse=True)
def clear_cache():
    from django.core.cache import caches

    caches["default"].clear()
    caches["other"].clear()
    caches["thread_local"].clear()
