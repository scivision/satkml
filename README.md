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
wget http://celestrak.com/NORAD/elements/gps-ops.txt
```

Example Use
-----------
```
python satplot.py gps-ops.txt 2015-04-29T16:00:00Z -k out.kml -l 65 -148 0 -p
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

[more examples](http://introtopython.org/visualization_earthquakes.html)
[API reference](http://matplotlib.org/basemap/)
![alt fancy plot](http://scienceopen.github.io/gpsconst.png)
![alt az/el plot](http://scienceopen.github.io/gpsazel.png)
