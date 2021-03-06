#!/usr/bin/env python
from __future__ import print_function, division
import argparse
import numpy as np
import matplotlib.pyplot as plot
from astropy import log
import astropy.units as u
from astropy.time import Time
from astropy.table import Table
from os import path
from matplotlib.colors import Normalize, LogNorm
from mpl_toolkits.basemap import Basemap

from nicer.values import *
from nicer.mcc import MCC
#from nicer.sps import SPS
from nicer.latloninterp import LatLonInterp

parser = argparse.ArgumentParser(description="Plot background info on a map")
parser.add_argument("bkffiles", help="Name of bkf files to process", nargs='+')
parser.add_argument("--column", help="Which bkf column to plot", default="EV_OVERSHOOT")
args = parser.parse_args()

log.info('Getting SAA data')
saa_lon, saa_lat = np.loadtxt(path.join(datadir,'saa_lonlat.txt'),unpack=True)
nph_lon, nph_lat = np.loadtxt(path.join(datadir,'nph_lonlat.txt'),unpack=True)
neph_lon, neph_lat = np.loadtxt(path.join(datadir,'neph_lonlat.txt'),unpack=True)
sph_lon, sph_lat = np.loadtxt(path.join(datadir,'sph_lonlat.txt'),unpack=True)


#Creating the plots and figure
log.info('plotting map')
fig = plot.figure(figsize = (11,8), facecolor = 'white')

#fig, ax = plot.subplots(figsize=(16,9))
plot.subplot(1,1,1)

map = Basemap(projection='cyl', resolution = 'l',  llcrnrlon=-180, llcrnrlat=-61,
urcrnrlon=180, urcrnrlat=61, lat_0 = 0, lon_0 = 0)
map.drawcoastlines()

if args.column == 'BAD_RATIO':
    vmin = 0.1
    vmax = 100.0
else:
    vmin = 5.0
    vmax = 100.0
for bk in args.bkffiles:
    bkftable = Table.read(bk,hdu=1)
    overshootrate = bkftable[args.column]
    sc = map.scatter(bkftable['LON'], bkftable['LAT'],c=overshootrate,
                     norm=LogNorm(vmin=vmin,vmax=vmax),cmap='jet',s=2.0)

map.plot(saa_lon,saa_lat,color='k',linestyle='dashed')
map.plot(nph_lon,nph_lat,color='k',linestyle='dotted')
map.plot(neph_lon,neph_lat,color='k',linestyle='dotted')
map.plot(sph_lon,sph_lat,color='k',linestyle='dotted')
cbar = map.colorbar(sc, location='bottom',pad='5%')
plot.title(args.column)

plot.show()
