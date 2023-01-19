from __future__ import division
import json
import pandas
import pickle
import pprint
import gpxpy.geo
import matplotlib.pyplot as plt
import numpy as np
import csv
import pytz
from timezonefinder import TimezoneFinder
from dateutil import tz
import math
import pandas
import datetime
import calendar
from itertools import groupby
from collections import defaultdict
import time

## define users' trajectories at cell spatial scale

data=pandas.read_csv('res_time.csv','r', delimiter=' ', \
                    header=None, names=['uid','created_at','coordinates','country_code'], skiprows=1, index_col=None, skipinitialspace=True,\
                    squeeze=False)

data=data[data.coordinates!="[0, 0]"] #remove entries with no precise coordinates, I'll need to compute distances based on these data

data = data.sort_values('created_at')

data = data.drop_duplicates(['uid','created_at'])

from collections import Counter

def more(x):
    paesi=[]
    c=Counter(x['country_code'])
    print c
    if len(c)>1:
        return True
    else: return False

data = data.groupby('uid').filter(lambda x: more(x)) #drop those who appear in only one country

print len(data)

print data.head()

def value(x):
    cc=x.split(",")
    cc0=cc[0].replace("[","")
    cc1=cc[1].replace("]","")
    x0,y0=float(cc0),float(cc1)
    return x0,y0

data['coordinates'] = data['coordinates'].apply(lambda x: value(x)) #reformat coordinates to feed them into the collocation function

data["created_at"] = data["created_at"].apply(lambda t: datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')) #to timetuple

data["created_at"] = data["created_at"].apply(lambda t: calendar.timegm(t.timetuple())) #to epoch time

data.set_index('uid', inplace=True)

from pyproj import Proj
myProj = Proj("+proj=eqc +lat_ts=0 +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +a=6371007 +b=6371007 +units=m +no_defs")
#get a projection that preserves distances

lat, lon=-15.790669, -47.892967 #example: Brasilia
xa, ya = myProj(lon, lat)
print xa,ya

import codecs
import heapq
import glob
import math
import numpy as np
import sys,os
import shapefile
import matplotlib.cm as cm
import matplotlib.patches as patches
from matplotlib.patches import Polygon, Circle, Rectangle
from matplotlib.collections import PatchCollection
from shapely.geometry import Point
from numpy import array

deltax=40000
sf = shapefile.Reader('/home/mattia/Tools/data/world/world4.shp') #read shapefile of grid cells made with Qgis in the same Equidistant projection, covered region is up to you
my_cmap = cm.get_cmap('Blues') #call colormap

shapes  = sf.shapes() #cells of the shapefile
Nshp    = len(shapes) #number of cells

print "len shapes"
print Nshp
shapes  = sf.shapes() #cells of the shapefile
Nshp    = len(shapes) #number of cells

centros=dict() #define cells centroids
xy=dict()

for nshp in xrange(Nshp): #as long as there are cells
    
    ww=0
    ptchs   = [] 
    pts     = array(shapes[nshp].points) #list of geographic points of every cell
    prt     = shapes[nshp].parts
    par     = list(prt) + [pts.shape[0]]
    
    centroid=[pts[0][0]+(pts[2][0]-pts[0][0])/2,pts[2][1]+(pts[0][1]-pts[2][1])/2]
    centros[nshp]=centroid

X=[]
Y=[]

for i in range(len(centros)):
    X.append(centros[i][0])
    Y.append(centros[i][1])
    
x0=shapes[0].points[0][0] #0 left-top 1 right-top 2 right-bottom 3 left_bottom
y0=shapes[0].points[0][1]
xmax=shapes[-1].points[1][0]
ymax=shapes[-1].points[2][1]

Lx=float("%.2f" % (xmax-x0))/deltax  #get height and width of the grid in terms of n of cells
Ly=float("%.2f" % (y0-ymax))/deltax

nx=int(Lx)
ny=int(Ly)

print 'n cells'
print nx,ny
print nx*ny,len(centros) #check that n of cells matches with n of centroids

def projection(x):
    x0,y0=myProj(x['coordinates'][0],x['coordinates'][1])
    return x0,y0

data[6] = data.apply(projection,axis=1)

def collocate(x):
    xi=x[0]
    yi=x[1]
    xx=int((xi-x0)/deltax) #num columns in the grid, get index to assign cell to each user's data-point
    yy=int((y0-yi)/deltax) #num rows

    if xx<0 or yy<0 or xx>nx or yy>ny:
        return 0 #will filter out next
    else:    
        a=np.ravel_multi_index((yy,xx), dims=(ny,nx),mode='clip') #(rows,cols)
        return a
                    
data['cell'] = data[6].apply(collocate)

data=data[data.cell!=0] #filter out those that fall out of the grid

monthsecs=2592000 #seconds in a month

traj=defaultdict(list) #dict of trajectories, keys are users, values are (cell, country, epoch time)

def traject(x):
    user=x.name
    for i in range(len(x)):
        pos=x['cell'].values[i]
        pais=x['country_code'].values[i]
        tiempo=x['created_at'].values[i]
        traj[user].append((pos,pais,tiempo))
    
data.groupby('uid').apply(lambda x: traject(x))

output = open('moreve2dist.pkl','wb') #save dict, we'll compute the radius of gyration with this
pickle.dump(traj, output)
output.close()
