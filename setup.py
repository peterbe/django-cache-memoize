from os import path
from setuptools import setup, find_packages

_here = path.dirname(__file__)


setup(
    name="django-cache-memoize",
    version="0.2.1",
    description=(
        "Django utility for a memoization decorator that uses the Django "
        "cache framework."
    ),
    long_description=open(path.join(_here, "README.rst")).read(),
    author="Peter Bengtsson",
    author_email="mail@peterbe.com",
    license="MPL-2.0",
    url="https://github.com/peterbe/django-cache-memoize",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment :: Mozilla",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords=["django", "memoize", "cache", "decorator"],
    zip_safe=False,
    extras_require={"dev": ["flake8", "tox", "twine", "therapist", "black"]},
)
