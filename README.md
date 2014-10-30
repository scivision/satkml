satkml
======

make KML of satellites

example download/usage. This example is for Fairbanks, Alaska on Oct 29, 2014 at 1600UT
```
cd ~
git clone https://github.com/scienceopen/satkml
curl -o ~/satkml/gps-ops.txt http://celestrak.com/NORAD/elements/gps-ops.txt
cd ~/satkml
python satplot.py gps-ops.txt 2014-10-29T16:00:00Z -k out.kml -l 65 -148 0
```

prerequisites: 
```
pip install pyephem simplekml pandas matplotlib dateutil numpy
```

optional prerequisites: for plotting world map overlay:
```
pip install basemap --allow-external basemap --allow-unverified basemap
```

[more examples](http://introtopython.org/visualization_earthquakes.html)
[API reference](http://matplotlib.org/basemap/)
![alt fancy plot](http://scienceopen.github.io/gpsconst.png)
![alt az/el plot](http://scienceopen.github.io/gpsazel.png)
