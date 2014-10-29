#!/usr/bin/env python3
from ephem import readtle,Observer,city
import simplekml as skml
from os.path import expanduser
from pdb import set_trace
from numpy import degrees,empty_like,nan
from pandas import date_range
from matplotlib.pyplot import figure,show
from matplotlib.ticker import MultipleLocator

def main(tle1,tle2,kmlfn):
    kmlfn = expanduser(kmlfn)    
#%% preallocation    
    forNhours = 12
    everyNminutes = 15    
    dates = date_range('2014-10-29T02:00:00',
                       periods=forNhours*60/everyNminutes+1,
                       freq=str(everyNminutes)+'T', tz='UTC')   
    lat = empty_like(dates,dtype=float)
    lon = empty_like(lat); alt_m = empty_like(lat)
    az = empty_like(lat); el = empty_like(lat)
#%% do work    
    obs = Observer()    
    obs.lat = 64.8; obs.lon = -147.7
    #obs = city('Seattle')
    sat = readtle('mySat',tle1, tle2)
    for i,d in enumerate(dates):
        obs.date = d
        sat.compute(obs)
        lat[i],lon[i],alt_m[i] = degrees(sat.sublat), degrees(sat.sublong), sat.elevation
        az[i], el[i] = degrees(sat.az), degrees(sat.alt)
        
    az[el<0] = nan; el[el<0] = nan
    
    
    ax = figure().gca()
    ax.plot(lon,lat,marker='.')
    ax.set_ylabel('lat [deg.]')
    ax.set_xlabel('lon [deg.]')
    ax.set_xlim(-180,180)
    ax.set_ylim(-90,90)
    ax.set_title(str(dates[0]) + ' to ' + str(dates[-1]))
    ax.grid(True)
    ax.yaxis.set_major_locator(MultipleLocator(15))
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.xaxis.set_major_locator(MultipleLocator(30))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    
    ax = figure().gca()
    ax.plot(az,el,marker='.')
    ax.set_xlabel('azimuth [deg.]')
    ax.set_ylabel('elevation [deg.]')
    show()
    
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='converts satellite position into KML for Google Earth viewing')
    p.add_argument('kmlfn',help='filename to save KML to',type=str,default=None)
    p.add_argument('line1',help='paste line 1 of TLE',type=str,nargs=9)    
    p.add_argument('line2',help='paste line 2 of TLE',type=str,nargs=8)
    args = p.parse_args()

    
    tle1 = ' '.join(args.line1)
    tle2 = ' '.join(args.line2)
    main(tle1,tle2,args.kmlfn)
    