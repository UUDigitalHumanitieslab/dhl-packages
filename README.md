# DHL-packages
Packages for python. Contains handy frequently used code.


## Requirements

Works with: python 3

## Creating a new package
See: https://python-packaging.readthedocs.io/en/latest/minimal.html

## Upload

1. Create dist
    1. `python setup.py sdist`
1. Upload dist with twine
    1. `twine upload dist/*`

## Install
`pip install dhlUtils`




## What is in it?

1. utilities for managing csv files
    1. loading and saving
    2. manipulating entries
1. Filesystem
    1. Currently only a function that can replace all strings in a file
