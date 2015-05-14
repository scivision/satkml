#!/usr/bin/env python3
"""
Initially designed to work with GPS satellites
"""
from __future__ import division
from ephem import readtle,Observer
from os.path import expanduser
from numpy import degrees,nan,isfinite,arange,radians
from pandas import date_range, DataFrame
from matplotlib.pyplot import figure,show
from matplotlib.ticker import MultipleLocator
from dateutil.parser import parse
from re import search

forNhours = 24
everyNminutes = 15

def loopsat(tlefn,date,kmlfn,obslla,satreq):
    obs = setupobs(obslla)
#%% preallocation
    if satreq is not None:
        dates = date_range(parse(date),
                           periods=forNhours*60/everyNminutes+1,
                           freq=str(everyNminutes)+'T')#, tz='UTC')
        data = DataFrame(index=dates,columns=['az','el','lat','lon','alt','srange'])
        sats,satnum = loadTLE(tlefn)
        try:
            sat = sats[satnum.index(satreq)]
        except ValueError as e:
            exit('i had trouble finding satellite {}.   {}'.format(satreq,e))
        satnum = satreq
        for d in dates:
            obs.date = d
            sat.compute(obs)
            data.at[d,['lat','lon','alt']] = degrees(sat.sublat), degrees(sat.sublong), sat.elevation
            data.at[d,['az','el','srange']] = degrees(sat.az), degrees(sat.alt),sat.range

        belowhoriz = data['el']<0
        data.ix[belowhoriz,['az','el','srange']] = nan
    else:
        dates = [parse(date)] #list for plotting
        data,satnum,belowhoriz = compsat(tlefn,obs,dates)

    return data,dates,satnum,belowhoriz,obs

def setupobs(lla):
    obs = Observer()
    try:
        obs.lat = str(lla[0]); obs.lon = str(lla[1]); obs.elevation=str(lla[2])
    except ValueError:
        print('observation location not specified. defaults to lat=0, lon=0')
    return obs

def compsat(tlefn,obs,dates):
    obs.date = dates[0]
    sats,satnum = loadTLE(tlefn)
    data = DataFrame(index=satnum,columns=['az','el','lat','lon','alt','srange'])

    for i,s in enumerate(sats):
        si = satnum[i]
        s.compute(obs)
        data.at[si,['lat','lon','alt']] = degrees(s.sublat), degrees(s.sublong), s.elevation
        data.at[si,['az','el','srange']] = degrees(s.az), degrees(s.alt), s.range

    belowhoriz = data['el']<0
    data.ix[belowhoriz,['az','el','srange']] = nan

    return data,satnum,belowhoriz

def fancyplot(lat,lon,dates,satnum):
    try:
        from mpl_toolkits.basemap import Basemap
    except ImportError as e:
        print('could not make fancy plot.  {}'.format(e))
        return
    #lon and lat cannot be pandas Series, must be values
    ax= figure().gca()
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
    m.plot(x,y,'o',color='#aaaaff',markersize=14)
    ax.set_title('GPS constellation at\n' + str(dates[0]))
    if not isinstance(satnum,list):
        satnum = [satnum]
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

def dokml(belowhoriz,lat,lon,alt_m,obs,kmlfn,satnum):
    if kmlfn is not None:
        try:
            import simplekml as skml
            kmlfn = expanduser(kmlfn)
            print('writing KML to ' + kmlfn)
            kml1d = skml.Kml()
            for s in satnum:
                if not belowhoriz[s]:
                    linestr = kml1d.newlinestring(name=str(s))
                    linestr.coords = [(obs.lon, obs.lat, obs.elevation),
                                      (lon[s], lat[s], alt_m[s])]
                    linestr.altitudemode = skml.AltitudeMode.relativetoground
            kml1d.save(kmlfn)
        except Exception as e:
            print('unable to write KML. Do you have simplekml package installed? ' + str(e))


def doplot(lat,lon,az,el,dates,satnum):
    polar = True

    fg = figure()
    ax1 = fg.gca()
    ax1.set_ylabel('lat [deg.]')
    ax1.set_xlabel('lon [deg.]')
    ax1.set_xlim(-180,180)
    ax1.set_ylim(-90,90)
    ax1.set_title('Latitude & Longitude starting\n' + str(dates[0]))
    ax1.grid(True)
    ax1.yaxis.set_major_locator(MultipleLocator(15))
    ax1.yaxis.set_minor_locator(MultipleLocator(5))
    ax1.xaxis.set_major_locator(MultipleLocator(30))
    ax1.xaxis.set_minor_locator(MultipleLocator(5))

    if polar:
        azoffs = 0#radians(3)
        az = radians(az.astype(float))
        el = 90-el.astype(float)
        ax2=figure().gca(polar=True)
        ax2.plot(az,el, marker='.',linestyle='')
        ax2.set_theta_zero_location('N')
        ax2.set_theta_direction(-1)
        ''' http://stackoverflow.com/questions/18721762/matplotlib-polar-plot-is-not-plotting-where-it-should '''
        ax2.set_yticks(range(0, 90+10, 10))                   # Define the yticks
        yLabel = ['90', '', '', '60', '', '', '30', '', '', '']
        ax2.set_yticklabels(yLabel)
    else:
        azoffs=3
        ax2 = figure().gca()
        ax2.plot(az,el,marker='.',linestyle='')
        ax2.set_xlabel('azimuth [deg.]')
        ax2.set_ylabel('elevation [deg.]')
        ax2.set_xlim(0,360)
        ax2.set_ylim(0,90)

    ax2.grid(True)


    ax1.plot(lon,lat,marker='.',linestyle='')

    if len(dates) !=1: #vs time case
        ax2.set_title('Azimuth & Elevation starting\n' + str(dates[0]))
        for i in range(lat.size):
            if isfinite(az[i]):
                ax2.text(az[i]+azoffs, el[i],
                         dates[i].strftime('%H:%M'),fontsize='small')
    else: # lots of sats case
        ax2.set_title('Azimuth & Elevation by PRN at\n' + str(dates[0]))
        for s in satnum:
            ax1.text(lon[s]+3, lat[s]+3,s,fontsize='small')
            if isfinite(az[s]):
                ax2.text(az[s]+azoffs, el[s],
                         s,fontsize='small')

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='converts satellite position into KML for Google Earth viewing')
    p.add_argument('tlefn',help='file with TLE to parse',type=str)
    p.add_argument('date',help='time to plot YYYY-mm-ddTHH:MM:SSZ',type=str)
    p.add_argument('--noplot',help='show plots',action='store_false')
    p.add_argument('-l','--lla',help='WGS84 lat lon [degrees] alt [meters] of observer',nargs=3,default=(None,None,None))
    p.add_argument('-k','--kmlfn',help='filename to save KML to',type=str,default=None)
    p.add_argument('--sat',help='satellite you want to pick from file',type=int,default=None)
    a = p.parse_args()
    showplot = a.noplot

    data,dates,satnum,belowhoriz,obs = loopsat(a.tlefn,a.date,a.kmlfn,a.lla,a.sat,)

    #%% basic plot
    if showplot:
        doplot(data['lat'],data['lon'],data['az'],data['el'],dates,satnum)
#%% write kml
    dokml(belowhoriz,data['lat'],data['lon'],data['alt'], obs, a.kmlfn,satnum)
#%% fancy plot
    if showplot:
        fancyplot(data['lat'].values,data['lon'].values,dates,satnum)

    show()