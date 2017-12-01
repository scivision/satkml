
======
satkml
======

Plot satellite az/el, and make KML of satellites for visualization in Google Earth.

.. contents::

Installation
============
::

    pip install -e .

.. image:: test/gpsconst.png
    :alt: GPS plot over lat long

.. image:: test/azel.png
    :alt: alt az/el plot

Examples
===========
The first argument "TLE" can be a URL pointing to a TLE, a filename containing TLE, or the TLE itself.
If you specify a URL, the program will download to the current directory and load it.

time instant
------------
::

    python satplot.py gps-ops.txt 2015-05-12T16:00:00 -k out.kml -c 65 -148 0


range of time
-------------
::

    python satplot.py gps-ops.txt 2015-05-12T16:00:00 2015-05-12T17:00:00 -c 65 -148 0

The main data product of the program is a 3-D pandas Panel ``data`` with dimensions time x satnum x parameter


Alternate, manual install (not needed for most users)
=====================================================
Most people do not need to do this::

    apt install libgeos-dev libgeos++-dev
    pip install basemap

Notes
=====
`basemap examples <http://introtopython.org/visualization_earthquakes.html>`_

`basemap API reference <http://matplotlib.org/basemap/>`_
