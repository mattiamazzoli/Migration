
# coding: utf-8

from __future__ import division
import json
import pandas
import pickle
import pprint
import gpxpy.geo
import matplotlib.pyplot as plt
import numpy as np
import csv
import time
import os
import glob

#WGS84 Web Mercator (Auxiliary Sphere)
from pyproj import Proj
myProj = Proj("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs")
#take a projection that preserves shapes, for bounding boxes

counter=0

with open('res_time.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')

    for filename in os.listdir('mostcommon_VE_VE_VE/'):  #directory with files regarding users classified as Venezuelan residents
        with open('mostcommon_VE_VE_VE/'+filename,'r') as documento: #parse all files
            for line in documento:
                tema=json.loads(line)

                if 'coordinates' in list(tema): #some have exact coordinates
                    b = tema
                    try:
                        a = (b['uid'],b['created_at'],b['coordinates'],b['place_country_code']) #coordinates will be lat lon here
                        writer.writerow(a)
                        
                    except:
                        counter+=1
                        print counter
                    
                elif 'place_bounding_box' in list(tema): #some have bounding boxes, so i take the center of it
                    
                    b = tema
                    try:
                        j = b['place_bounding_box'][0][0]
                        k = b['place_bounding_box'][0][1]
                        h = b['place_bounding_box'][0][2]
                        g = b['place_bounding_box'][0][3]
                        jj=myProj(j[0],j[1]) #get projection of each bound
                        kk=myProj(k[0],k[1])
                        hh=myProj(h[0],h[1])
                        gg=myProj(g[0],g[1])
                        x1=np.abs(jj[0]-kk[0])
                        x2=np.abs(jj[0]-hh[0])
                        x3=np.abs(jj[0]-gg[0])
                        x4=np.abs(kk[0]-hh[0])
                        x5=np.abs(kk[0]-gg[0])
                        x6=np.abs(hh[0]-gg[0])
                        y1=np.abs(jj[1]-kk[1])
                        y2=np.abs(jj[1]-hh[1])
                        y3=np.abs(jj[1]-gg[1])
                        y4=np.abs(kk[1]-hh[1])
                        y5=np.abs(kk[1]-gg[1])
                        y6=np.abs(hh[1]-gg[1])
                        if np.max([x1,x2,x3,x4,x5,x6,y1,y2,y3,y4,y5,y6])<40000: #I want shapes and diagonals with sides less than 40km long
                            centerx=(j[0]+k[0]+h[0]+g[0])/4 #get the center
                            centery=(j[1]+k[1]+h[1]+g[1])/4
                            
                            a = (b['uid'],b['created_at'],[centerx,centery],b['place_country_code']) #warning, coordinates are not lat lon here
                            writer.writerow(a)
                        else:
                            a = (b['uid'],b['created_at'],[0,0],b['place_country_code']) #set coords to zero to filter them out later, still I need the country to compute appearances
                            writer.writerow(a)
                    except:
                        counter+=1 #count exceptions
                        print counter,'o'



