import pytest

from django.core.cache import caches


@pytest.fixture(autouse=True)
def clear_cache():
    caches['default'].clear()
