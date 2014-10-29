satkml
======

make KML of satellites

example download/usage:
```
cd ~
git clone https://github.com/scienceopen/satkml
curl -o ~/satkml/gps-ops.txt http://celestrak.com/NORAD/elements/gps-ops.txt
cd ~/satkml
python satplot.py gps-ops.txt 2014-10-29T16:00:00Z -k out.kml
```

prerequisites: 
```
pip install pyephem simplekml pandas matplotlib dateutil numpy
```
