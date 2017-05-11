from re import search
from urllib.request import urlretrieve
import simplekml as skml
from sys import stderr
from ephem import readtle,Observer
from pathlib import Path
from numpy import degrees,nan
from pandas import  DataFrame,Panel



def loopsat(tlefn, dates, obs):
    cols = ['az','el','lat','lon','alt','srange']
    sats,satnum = loadTLE(tlefn)

    data = Panel(items=dates, major_axis=satnum, minor_axis=cols)
    for d in dates:
        obs.date = d

        df = DataFrame(index=satnum, columns=cols)
        for i,s in enumerate(sats):
            s.compute()  # don't compute lat/lon/alt with obs! will give wrong answer!
            df.at[satnum[i], ['lat','lon','alt']] = degrees(s.sublat), degrees(s.sublong), s.elevation
            s.compute(obs)
            df.at[satnum[i], ['az','el','srange']] = degrees(s.az), degrees(s.alt), s.range

        df.ix[df['el'] < 0 ,['az','el','srange']] = nan

        data[d] = df

    return data

def setupobs(obslla):
    assert len(obslla) == 3
    obs = Observer()
    obs.lat = str(obslla[0])  # STRING or wrong result! degrees
    obs.lon = str(obslla[1])  # STRING or wrong result! degrees
    obs.elevation=obslla[2]  # meters

    return obs

def loadTLE(tlefn):
    """ Loads a TLE file and creates a list of satellites.
    http://blog.thetelegraphic.com/2012/gps-sattelite-tracking-in-python-using-pyephem/
    """
    pat = r'(?<=PRN)\s*\d\d'
    # pat = '(?<=PRN)\d\d'
    prn = []
    satlist = []

    if '\n' in tlefn:  # assume it IS the TLE
        tle = tlefn
        tle = tle.split('\n')
        satlist.append(readtle(tle[0], tle[1], tle[2]))
        if 'PRN' in satlist[0].name:  # assume GPS
            prn.append(int(search(pat,satlist[0].name).group()))
    elif tlefn.startswith('http') or tlefn.startswith('ftp'):  # assume URL
        tleout = tlefn.split('/')[-1]
        print('saving TLE to',tleout)
        urlretrieve(tlefn, tleout)
        return loadTLE(tleout)
    else:  # assume filename
        tlefn = Path(tlefn).expanduser()

        with tlefn.open('r') as f:
            satlist = []; prn = []
            l1 = f.readline()
            while l1:
                l2 = f.readline()
                l3 = f.readline()
                sat = readtle(l1,l2,l3)
                satlist.append(sat)
                if 'PRN' in sat.name:  # assume GPS
                    prn.append(int(search(pat,sat.name).group()))
                l1 = f.readline()

    return satlist,prn

def dokml(data, obs, kmlfn):
    # TODO: make this work with multiple times properly (show animated paths)
    # right now it just overwrites the kml file until it reaches the last time.
    if kmlfn is not None:
      try:
          for t,d in data.items():
              lat= d['lat']; lon= d['lon']; alt_m = d['alt']
              satnum = d.index

              kmlfn = Path(kmlfn).expanduser()
              kml1d = skml.Kml()
              for s in satnum:
                  if not belowhoriz[s]:
                      linestr = kml1d.newlinestring(name='PRN{:d}'.format(s))
                      linestr.coords = [(obs.lon, obs.lat, obs.elevation),
                                        (lon[s], lat[s], alt_m[s])]
                      linestr.altitudemode = skml.AltitudeMode.relativetoground
              kml1d.save(str(kmlfn))
      except Exception as e:
          print('unable to write KML. Do you have simplekml package installed?',e,file=stderr)
