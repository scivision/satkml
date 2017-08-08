#!/usr/bin/env python
req = ['python-dateutil','ephem','pandas','matplotlib','numpy','basemap',]
pipreq=['simplekml']
# %%
import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:
    pip.main(['install'] + req)
pip.main(['install'] + pipreq)
# %% install
from setuptools import setup

setup(name='satkml',
      packages=['satkml'],
      author='Michael Hirsch, Ph.D.',
      description='Plots numerous satellites in Matplotlib and to KML for Google Earth',
      version='0.5',
      install_requires=pip+pipreq,
      )
