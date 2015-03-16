"""
This file is a hack for Datajoy.com, it is not for use on your own PC
"""

import os
os.system("sudo conda install ephem basemap")

os.system('python satplot.py gps-ops.txt 2014-10-29T16:00:00Z -p')