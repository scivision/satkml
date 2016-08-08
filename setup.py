#!/usr/bin/env python
from setuptools import setup
import subprocess

try:
    subprocess.call(['conda','install','--file','requirements.txt'])
except Exception as e:
    pass

#%% install
setup(name='satkml',
      description='Plot satellite tracks in KML',
      author='Michael Hirsch',
      url='https://github.com/scienceopen/satkml',
      install_requires=['pathlib2','simplekml'],
      packages=['satkml']
      )
