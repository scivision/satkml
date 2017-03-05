#!/usr/bin/env python
from setuptools import setup

# NOTE: when basemap-1.1 is released, it may be on Pypi again.
req = ['python-dateutil','ephem','pandas','matplotlib','numpy','basemap',
       'simplekml',
       'https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz']
#%% install
setup(name='satkml',
      packages=['satkml'],
      author='Michael Hirsch, Ph.D.',
      description='Plots numerous satellites in Matplotlib and to KML for Google Earth',
      version='0.5',
      install_requires=req,
      )
