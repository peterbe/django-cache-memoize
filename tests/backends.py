from collections import OrderedDict
from django.core.cache.backends.locmem import LocMemCache

try:
    # For Django versions < 2.1
    from django.utils.synch import RWLock as Lock
except ImportError:
    from threading import Lock


class ThreadLocalCache(LocMemCache):
    def __init__(self, *args, **kwargs):
        """
        Same implementation as LocMemCache, except for initialization

        We create the cache as a member of this class, so it only lasts
        as long as the cache backend lasts.
        """
        self._cache = OrderedDict()
        self._expire_info = {}
        self._lock = Lock()

        # NB: This is not calling LocMemCache.__init__
        # - it skips to its parent instead
        super(LocMemCache, self).__init__({})
