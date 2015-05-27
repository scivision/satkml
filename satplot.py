#!/usr/bin/env python3
"""
Initially designed to work with GPS satellites
see README.md for examples and explanation

output:
-------
data: a pandas 3-D Panel with dimensions time x satnum x parameter
"""
from __future__ import division
from ephem import readtle,Observer
from os.path import expanduser
from numpy import degrees,nan,isfinite,arange,radians
from pandas import date_range, DataFrame,Panel
from matplotlib.pyplot import figure,show
from matplotlib.ticker import MultipleLocator
from dateutil.parser import parse
from re import search
from warnings import warn
from six import string_types
try:
    import simplekml as skml
except ImportError as e:
    warn('cannot write KML. pip install simplekml   {}'.format(e))
#
try:
    import seaborn as sns
    sns.set(context='talk', style='whitegrid')
except ImportError as e:
    warn('disabling advanced plotting. pip install seaborn   {}'.format(e))

def loopsat(tlefn,dates,kmlfn,obslla):
    obs = setupobs(obslla)

    data,belowhoriz = compsat(tlefn,obs,dates)

    return data,obs,belowhoriz

def setupobs(lla):
    obs = Observer()
    try:
        obs.lat = str(lla[0]); obs.lon = str(lla[1]); obs.elevation=float(lla[2])
    except ValueError:
        warn('observation location not specified. defaults to lat=0, lon=0')
    return obs

def compsat(tlefn,obs,dates):
    cols = ['az','el','lat','lon','alt','srange']
    sats,satnum = loadTLE(tlefn)

    data = Panel(items=dates, major_axis=satnum, minor_axis=cols)
    for d in dates:
        obs.date = d

        df = DataFrame(index=satnum,columns=cols)
        for i,s in enumerate(sats):
            si = satnum[i]
            s.compute(obs)
            df.at[si,['lat','lon','alt']] = degrees(s.sublat), degrees(s.sublong), s.elevation
            df.at[si,['az','el','srange']] = degrees(s.az), degrees(s.alt), s.range

        belowhoriz = df['el']<0
        df.ix[belowhoriz,['az','el','srange']] = nan

        data[d] = df

    return data,belowhoriz

def fancyplot(data):
    try:
        from mpl_toolkits.basemap import Basemap
    except ImportError as e:
        warn('could not make fancy plot.  {}'.format(e))
        return

    dates = data.items.values
    satnum = data.major_axis
    if dates.size>6:
        warn('skipping fancy map plot due to too many times (plot will get overly crowded)')
        return
    #lon and lat cannot be pandas Series, must be values
    for d in data:
        lat= data[d]['lat'].values; lon= data[d]['lon'].values
        ax= figure(3).gca()
        m = Basemap(projection='merc',
                      llcrnrlat=-80, urcrnrlat=80,
                      llcrnrlon=-180,urcrnrlon=180,
                      lat_ts=20,
                      resolution='c')

        m.drawcoastlines()
        m.drawcountries()
        m.drawmeridians(arange(0,360,30))
        m.drawparallels(arange(-90,90,30))
        x,y = m(lon,lat)
        m.plot(x,y,'o',color='#dadaff',markersize=14)
        ax.set_title('GPS constellation \nfrom {} to {}'.format(dates[0],dates[-1]))

        for s,xp,yp in zip(satnum,x,y):
            ax.text(xp,yp,s,ha='center',va='center',fontsize=11)


def loadTLE(filename):
    """ Loads a TLE file and creates a list of satellites.
    http://blog.thetelegraphic.com/2012/gps-sattelite-tracking-in-python-using-pyephem/
    """
    #pat = '(?<=PRN)\d\d'
    with open(filename) as f:
        satlist = []; prn = []
        l1 = f.readline()
        while l1:
            l2 = f.readline()
            l3 = f.readline()
            sat = readtle(l1,l2,l3)
            satlist.append(sat)

            prn.append(int(search(r'(?<=PRN)\s*\d\d',sat.name).group()))
            l1 = f.readline()

    return satlist,prn

def dokml(belowhoriz,data,obs,kmlfn):
    # TODO: make this work with multiple times properly (show animated paths)
    # right now it just overwrites the kml file until it reaches the last time.
    if kmlfn is not None:
      try:
          for t,d in data.iteritems():
              lat= d['lat']; lon= d['lon']; alt_m = d['alt']
              satnum = d.index

              kmlfn = expanduser(kmlfn)
              kml1d = skml.Kml()
              for s in satnum:
                  if not belowhoriz[s]:
                      linestr = kml1d.newlinestring(name='PRN{:d}'.format(s))
                      linestr.coords = [(obs.lon, obs.lat, obs.elevation),
                                        (lon[s], lat[s], alt_m[s])]
                      linestr.altitudemode = skml.AltitudeMode.relativetoground
              kml1d.save(kmlfn)
      except Exception as e:
          warn('unable to write KML. Do you have simplekml package installed? ' + str(e))


def doplot(data,obs):
  polar = True

  dates = data.items
  satnum= data.major_axis

  for s in satnum:
    az = data.ix[:,s,'az'].values;  el = data.ix[:,s,'el'].values
    lat= data.ix[:,s,'lat'].values; lon= data.ix[:,s,'lon'].values #need .values for indexing

    fg = figure(1)
    ax1 = fg.gca()
    ax1.set_ylabel('lat [deg.]')
    ax1.set_xlabel('lon [deg.]')
    ax1.set_xlim(-180,180)
    ax1.set_ylim(-90,90)
    ax1.set_title('Latitude & Longitude from\n{} to {}'.format(dates[0].strftime('%xT%X'), dates[-1].strftime('%xT%X')))
    #ax1.grid(True)
    ax1.yaxis.set_major_locator(MultipleLocator(15))
    ax1.yaxis.set_minor_locator(MultipleLocator(5))
    ax1.xaxis.set_major_locator(MultipleLocator(30))
    ax1.xaxis.set_minor_locator(MultipleLocator(5))

    if polar:
        azoffs = 0#radians(3)
        az = radians(az.astype(float))
        el = 90-el.astype(float)
        ax2=figure(2).gca(polar=True)
        ax2.plot(az,el, marker='.',linestyle='-')
        ax2.set_theta_zero_location('N')
        ax2.set_theta_direction(-1)
        ''' http://stackoverflow.com/questions/18721762/matplotlib-polar-plot-is-not-plotting-where-it-should '''
        ax2.set_yticks(range(0, 90+10, 10))                   # Define the yticks
        yLabel = ['90', '', '', '60', '', '', '30', '', '', '']
        ax2.set_yticklabels(yLabel)
    else:
        azoffs=3
        ax2 = figure(2).gca()
        ax2.plot(az,el,marker='.',linestyle='-')
        ax2.set_xlabel('azimuth [deg.]')
        ax2.set_ylabel('elevation [deg.]')
        ax2.set_xlim(0,360)
        ax2.set_ylim(0,90)

    #ax2.grid(True)

    ax1.plot(lon,lat,marker='.',linestyle='-')
    ax2.set_title('Azimuth & Elevation by PRN @ ({},{}) from\n{} to {}'.format(obs.lat,obs.lon,dates[0],dates[-1]))

    if len(dates)<6: #don't want overcrowded plot
        for i,d in enumerate(dates):
                pl = '{} {}'.format(s, d.strftime('%H:%M'))
                ax1.text(lon[i]+3, lat[i]+3,pl,fontsize='x-small')
                if isfinite(az[i]):
                    ax2.text(az[i]+azoffs, el[i],pl,fontsize='x-small')
    else: #just label first point
        #too much text for all satellites and all times (maybe label once per line)
        ax1.text(lon[0]+3, lat[0]+3,s,fontsize='small')
        if isfinite(az[0]):
            ax2.text(az[0]+azoffs, el[0],
                 s,fontsize='small')

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='converts satellite position into KML for Google Earth viewing')
    p.add_argument('tlefn',help='file with TLE to parse',type=str)
    p.add_argument('-d','--date',help='start/stop time to start 24 hour plot YYYY-mm-ddTHH:MM:SSZ',nargs='+',type=str,default='')
    p.add_argument('-T','--period',help='time interval (MINUTES) to compute sats. position (default=15 min)',type=str,default='15')
    p.add_argument('--noplot',help='show plots',action='store_false')
    p.add_argument('-l','--lla',help='WGS84 lat lon [degrees] alt [meters] of observer',nargs=3,default=(None,None,None))
    p.add_argument('-k','--kmlfn',help='filename to save KML to',type=str,default=None)
    a = p.parse_args()
    showplot = a.noplot

#%% setup dates
    if len(a.date) == 1 or isinstance(a.date,string_types):
        dates = [parse(a.date)]
    elif len(a.date) ==2:
        dates = date_range(start=a.date[0], end=a.date[1],  freq='{}T'.format(a.period))
    else:
        raise ValueError('specify one date, or two (start/stop) dates')
#%% do computation
    data,obs,belowhoriz = loopsat(a.tlefn,dates,a.kmlfn,a.lla)
#%% basic plot
    if showplot:
        doplot(data,obs)
#%% write kml
    dokml(belowhoriz,data, obs, a.kmlfn)
#%% fancy plot
    if showplot:
        fancyplot(data)

    show()