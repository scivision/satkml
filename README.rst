[![Code Climate](https://codeclimate.com/github/scienceopen/satkml/badges/gpa.svg)](https://codeclimate.com/github/scienceopen/satkml)

======
satkml
======

Plot satellite az/el, and make KML of satellites for visualization in Google Earth.

Installation
-------------
.. code-block:: bash

    git clone https://github.com/scienceopen/satkml
    conda install --file requirements.txt
    pip install simplekml

.. image:: http://scienceopen.github.io/gpsconst.png
    :alt: GPS plot over lat long

.. image:: azel.png
    :alt: alt az/el plot

Example Use
-----------
You need to have the ephemeris files for the satellite(s) you want to plot.
In this example I'm using GPS satellites.
You can manually download ephemeris from `Dr. Kelso's Celestrack website <http://www.celestrak.com/webmaster.asp>`_ via your web browser, or use curl or wget::

    wget http://celestrak.com/NORAD/elements/gps-ops.txt


Plot satellites at one time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    python satplot.py gps-ops.txt 2015-05-12T16:00:00 -k out.kml -l 65 -148 0


Plot satellites for a range of time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    python satplot.py gps-ops.txt 2015-05-12T16:00:00 2015-05-12T17:00:00 -l 65 -148 0

The main data product of the program is a 3-D pandas Panel named "data" with dimensions time x satnum x parameter


Alternate, manual install (not needed for most users)
-----------------------------------------------------
Most peopl do not need to do this::

    sudo apt-get install libgeos-dev libgeos++-dev
    pip install basemap --allow-external basemap --allow-unverified basemap

or if that doesn't work for you installing basemap, try::

    sudo apt-get install python-mpltoolkits.basemap python-mpltoolkits.basemap-data

matplotlib basemap references
-----------------------------
`basemap examples <http://introtopython.org/visualization_earthquakes.html>`_

`basemap API reference <http://matplotlib.org/basemap/>`_


