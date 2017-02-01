#!/usr/bin/env python
from setuptools import setup
try:
    import conda.cli
    conda.cli.main('install','--file','requirements.txt')
except Exception as e:
    print(e)

#%% install
setup(name='satkml',
      install_requires=['simplekml'],
      packages=['satkml']
      )
