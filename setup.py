#!/usr/bin/env python
install_requires = ['python-dateutil','ephem','pandas','matplotlib','numpy','basemap','simplekml']

# %% install
from setuptools import setup,find_packages

setup(name='satkml',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      description='Plots numerous satellites in Matplotlib and to KML for Google Earth',
      version='0.5.0',
      install_requires=install_requires,
      python_requires='>=3.5',
      )
