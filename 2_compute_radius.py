from __future__ import division
import json
import pandas
import pickle
import pprint
import matplotlib.pyplot as plt
import numpy as np
import pandas
import datetime
from collections import defaultdict
import matplotlib as mpl
import matplotlib.pyplot as plt

pkl_file = open('moreve2dist.pkl','rb')
traj = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('worldcentros4dist.pkl','rb') #centroids of the shapefile made with the Equidistant projection
centros = pickle.load(pkl_file)
pkl_file.close()

cm=dict()
for i in traj.keys(): #keys are users
    n=0
    x=0
    y=0
    for j in traj[i]: #for each of their datapoints
        x+=centros[j[0]][0]
        y+=centros[j[0]][1]
        n+=1
    cm[i]=(x/n,y/n,n)  #compute center of mass of each user

rg=dict()
for i in traj.keys(): #now I can compute the radius of gyration
    n=0
    d=0
    xc=cm[i][0]
    yc=cm[i][1]
    n=cm[i][2]
    for j in traj[i]: #tweets
        xd=centros[j[0]][0]-xc
        yd=centros[j[0]][1]-yc
        d+= xd**2 + yd**2
    rg[i]=np.sqrt(d/n)
        
output = open('rgworld.pkl','wb') #filter on radius of gyration will be applied on this distribution
pickle.dump(rg, output)
output.close()
