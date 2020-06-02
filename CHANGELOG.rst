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
