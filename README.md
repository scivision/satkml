[![Code Health](https://landscape.io/github/scienceopen/satkml/master/landscape.png)](https://landscape.io/github/scienceopen/satkml/master)

satkml
======

Plot satellite az/el, and make KML of satellites for visualization in Google Earth.

Installation:
-------------
```
git clone https://github.com/scienceopen/satkml
conda install --file requirements.txt
pip install simplekml
```

![alt fancy plot](http://scienceopen.github.io/gpsconst.png)

![alt az/el plot](http://scienceopen.github.io/gpsazel.png)

Example Use
-----------
You need to have the ephemeris files for the satellite(s) you want to plot.
In this example I'm using GPS satellites.
You can manually download ephemeris from [Dr. Kelso's](http://www.celestrak.com/webmaster.asp) Celestrack website via your web browser, or use curl or wget.
```
wget http://celestrak.com/NORAD/elements/gps-ops.txt
```

Plot all satellites at one time:
```
python satplot.py gps-ops.txt 2015-04-29T16:00:00Z -k out.kml -l 65 -148 0 -p
```

Plot one satellite for a range of time:
```
python satplot.py gps-ops.txt 2015-04-29T16:00:00Z -p --sat 32
```
------------------------------------------------------------

Alternate, manual install (not needed for most users)
-----------------------------------------------------
```
sudo apt-get install libgeos-dev libgeos++-dev
pip install basemap --allow-external basemap --allow-unverified basemap
```
or if that doesn't work for you installing basemap, try:
```
sudo apt-get install python-mpltoolkits.basemap python-mpltoolkits.basemap-data
```

matplotlib basemap references
-----------------------------
[basemap examples](http://introtopython.org/visualization_earthquakes.html)

[basemap API reference](http://matplotlib.org/basemap/)


