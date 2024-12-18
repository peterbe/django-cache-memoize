0.2.1
~~~~~~

- The ``timeout`` value is now optional and defaults to that of
  ``DEFAULT_TIMEOUT`` from ``django.core.cache.backends.base``
  `pull#68 <https://github.com/peterbe/django-cache-memoize/pull/68>`

0.1.11
~~~~~~

- Include 3.12 in tests and omit 3.8
  `pull#69 <https://github.com/peterbe/django-cache-memoize/pull/69>`

0.1.10
~~~~~~

- Support for Django 3.2
  `pull#51 <https://github.com/peterbe/django-cache-memoize/pull/51>`
  Thanks @UsamaSadiq

0.1.9
~~~~~

- Fix potential problem with default cache key generation (sort order,
  possible identical key, quoting of paramters with ``=`` sign in string)
  `pull#50 <https://github.com/peterbe/django-cache-memoize/pull/50>`_
  Thanks @kri-k

0.1.8
~~~~~

- New `get_cache_key` method for findout out what a decorated function's
  cache key would be.
  `pull#44 <https://github.com/peterbe/django-cache-memoize/pull/44>`_
  Thanks @benweatherman

0.1.7
~~~~~

- Use a functions's ``__qualname__`` instead to avoid clases with functions
  of the same name.
  `pull#41 <https://github.com/peterbe/django-cache-memoize/pull/41>`_

0.1.6
~~~~~

- Fetch cache backend later to provide thread-safety
  `pull#21 <https://github.com/peterbe/django-cache-memoize/pull/21>`_

- Fix cache invalidation with custom key generator
  `pull#20 <https://github.com/peterbe/django-cache-memoize/pull/20>`_

0.1.5
~~~~~

- Fix when using ``_refresh=False`` and the ``.invalidate()``.
  `pull#19 <https://github.com/peterbe/django-cache-memoize/pull/19>`_

0.1.4
~~~~~

- Ability to have the memoized function return ``None`` as an actual result.
  `pull#9 <https://github.com/peterbe/django-cache-memoize/pull/9>`_

0.1.3
~~~~~

- Ability to pass in your own custom cache-key callable function.
  Thanks @jaumebecks
  `pull#10 <https://github.com/peterbe/django-cache-memoize/pull/10>`_

0.1.2
~~~~~

- Ability to specify a different-than-default cache alias
  Thanks @benspaulding
  `pull#6 <https://github.com/peterbe/django-cache-memoize/pull/6>`_

0.1.1
~~~~~

- Package sit-ups. Main file not a package so it wasn't distributed.

0.1.0
^^^^^

- Basic version released.
