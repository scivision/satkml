#!/usr/bin/env python3
#from pdb import set_trace
from __future__ import division
from ephem import readtle,Observer
from os.path import expanduser
from numpy import degrees,nan,isnan,arange
from pandas import date_range, DataFrame
from matplotlib.pyplot import figure,show,gca
from matplotlib.ticker import MultipleLocator
from dateutil.parser import parse
from re import search

def main(tlefn,date,kmlfn,obslla,satreq, showplot):
    obs = Observer()
    try:
        obs.lat = str(obslla[0]); obs.lon = str(obslla[1])
        obs.elevation=str(obslla[2])
    except ValueError:
        print('observation location not specified. defaults to lat=0, lon=0')
#%% preallocation
    if satreq is not None:
        forNhours = 12
        everyNminutes = 15
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
        for i,d in enumerate(dates):
            obs.date = d
            sat.compute(obs)
            data.ix[i,'lat'] = degrees(sat.sublat)
            data.ix[i,'lon'] = degrees(sat.sublong)
            data.ix[i,'alt'] = sat.elevation
            data.ix[i,'az'], data.ix[i,'el'] = degrees(sat.az), degrees(sat.alt)
            data.ix[i,'srange'] = sat.range
    else:
        dates = [parse(date)]
        obs.date = dates[0]
        sats,satnum = loadTLE(tlefn)
        data = DataFrame(index=satnum,columns=['az','el','lat','lon','alt','srange'])

        for i,s in enumerate(sats):
            si = satnum[i]
            s.compute(obs)
            data.ix[si,'lat'] = degrees(s.sublat)
            data.ix[si,'lon'] = degrees(s.sublong)
            data.ix[si,'alt'] = s.elevation
            data.ix[si,'az'] = degrees(s.az)
            data.ix[si,'el'] = degrees(s.alt)
            data.ix[si,'srange'] = s.range

    belowhoriz = data['el']<0
    data.ix[belowhoriz,['az','el','srange']] = nan
#%% basic plot
    if showplot:
        doplot(data['lat'],data['lon'],data['az'],data['el'],dates,satnum)
#%% write kml
    dokml(belowhoriz,data['lat'],data['lon'],data['alt'],
          obs, kmlfn,satnum)
#%% fancy plot
    if showplot:
        fancyplot(data['lat'].values,data['lon'].values,dates,satnum)

    return data

def fancyplot(lat,lon,dates,satnum):
    #lon and lat cannot be pandas Series, must be values
    try:
        from mpl_toolkits.basemap import Basemap
        m = Basemap(projection='merc',
                      llcrnrlat=-80,urcrnrlat=80,
                      llcrnrlon=-180,urcrnrlon=180,
                      lat_ts=20,
                      resolution='c')

        m.drawcoastlines()
        m.drawcountries()
        m.drawmeridians(arange(0,360,30))
        m.drawparallels(arange(-90,90,30))
        x,y = m(lon,lat)
        m.plot(x,y,'o',color='#aaaaff',markersize=14)
        ax = gca()
        ax.set_title('GPS constellation at\n' + str(dates[0]))
        for s,xp,yp in zip(satnum,x,y):
            ax.text(xp,yp,s,ha='center',va='center',fontsize=11)
        show()
    except ImportError as e:
        print('could not make fancy plot  ' + str(e))


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

    print('{} satellites loaded into list'.format(len(satlist)))
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
    polar =False

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
        ax2=figure().gca(polar=True)
        ax2.set_theta_zero_location('N')
        ax2.set_theta_direction(-1)
    else:
        ax2 = figure().gca()
        ax2.set_xlabel('azimuth [deg.]')
        ax2.set_ylabel('elevation [deg.]')
        ax2.set_xlim(0,360)
        ax2.set_ylim(0,90)

    ax2.grid(True)


    if len(dates) !=1: #vs time case
        ax1.plot(lon,lat,marker='.')
        ax2.plot(az,el,marker='.')
        ax2.set_title('Azimuth & Elevation starting\n' + str(dates[0]))
        for i in range(lat.size):
            if not isnan(az[i]):
                ax2.text(az[i]+3,el[i],dates[i].strftime('%H:%M'),fontsize=8)
    else: # lots of sats case
        ax1.plot(lon,lat,marker='.',linestyle='')
        ax2.plot(az,el,marker='.',linestyle='')
        ax2.set_title('Azimuth & Elevation by PRN at\n' + str(dates[0]))
        for s in satnum:
            ax1.text(lon[s]+3,lat[s]+3,s,fontsize=10)
            if not isnan(az[s]):
                ax2.text(az[s]+3,el[s],s,fontsize=10)


    show()

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='converts satellite position into KML for Google Earth viewing')
    p.add_argument('tlefn',help='file with TLE to parse',type=str)
    p.add_argument('date',help='time to plot YYYY-mm-ddTHH:MM:SSZ',type=str)
    p.add_argument('-p','--plot',help='show plots',action='store_true')
    p.add_argument('-l','--lla',help='WGS84 lat lon [degrees] alt [meters] of observer',nargs=3,default=(None,None,None))
    p.add_argument('-k','--kmlfn',help='filename to save KML to',type=str,default=None)
    p.add_argument('--sat',help='satellite you want to pick from file',type=int,default=None)
    a = p.parse_args()

    data = main(a.tlefn,a.date,a.kmlfn,a.lla,a.sat,a.plot)

