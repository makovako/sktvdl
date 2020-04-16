# SKTVDL

A SKTVDL is a small program/script for downloading videos from television online archives in Slovakia. Just run the *sktvdl.py* program and pass url of a page with the video as a CLI argument.

# TODO

- TVs archives
  - JOJ
- live
  - markiza
  - doma
  - dajto
  - rtvs
    - 1
    - 2
  - joj
  - plus
  - wau
  - ta3

# Notes

- structure for setuptools
- requirements.txt (for development) vs setup dependncies (for installation)
- in packagename dir put `__init__.py` file and create method to be executed
- complete `setup.py`
  - `install_requires` - dependencies
  - for cli execution after installation
```py
entry_points={
    'console_scripts' : [
        'sktvdl = sktvdl:main'
    ]
},
```
- Changelog
  - extension for vscode
  - unified structure for changes
  - keeps changes for history, makes it easy to create releases