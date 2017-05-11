#!/usr/bin/env python
"""
Initially designed to work with GPS satellites
see README.md for examples and explanation

output:
-------
data: a pandas 3-D Panel with dimensions time x satnum x parameter
"""
from __future__ import print_function
from pandas import date_range
from datetime import datetime
from dateutil.parser import parse
from matplotlib.pyplot import show
import seaborn as sns
sns.set(context='talk', style='whitegrid')
#
from satkml import loopsat, dokml, setupobs
from satkml.plots import doplot, fancyplot

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='converts satellite position into KML for Google Earth viewing')
    p.add_argument('tle',help='TLE, TLE file, or TLE URL')
    p.add_argument('-d','--date',help='start/stop time to start 24 hour plot YYYY-mm-ddTHH:MM:SSZ',nargs='+',default=[datetime.utcnow()])
    p.add_argument('-T','--period',help='time interval (MINUTES) to compute sats. position (default=15 min)',type=int,default=15)
    p.add_argument('-c','--lla',help='WGS84 lat lon [degrees] alt [meters] of observer',nargs=3,type=float,default=[65.1,-147.5,0])
    p.add_argument('-k','--kmlfn',help='filename to save KML to')
    p = p.parse_args()
#%% setup dates
    if len(p.date) == 1:
        if isinstance(p.date, str):
            dates = [parse(p.date)]
        else:
            dates = p.date
    elif len(p.date) ==2:
        dates = date_range(start=p.date[0], end=p.date[1],  freq='{}T'.format(p.period))
#%% do computation
    obs = setupobs(p.lla)
    data = loopsat(p.tle, dates, obs)
#%% basic plot
    doplot(data, obs)
#%% write kml
    dokml(data, obs, p.kmlfn)
#%% fancy plot
    fancyplot(data)

    show()
