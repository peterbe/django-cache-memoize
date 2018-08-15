#!/bin/bash
set -e

rm -fr dist/*
python setup.py sdist
twine upload dist/*
