
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
import math
import pandas
import datetime
import calendar
from itertools import groupby

pkl_file = open('moreve2country.pkl','rb') #users appearing abroad at least once
data = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('bad.pkl','rb') #list of users with higher radius of gyration than the threshold
bad = pickle.load(pkl_file)
pkl_file.close()

south=['AI','AR','AW','BB','BL','BM','BO','BR','BS','BZ','CL','CO','CR','CU','CW','DM','DO','EC','FK','GP','GT','GY','HN','HT','JM','KN','KY','LC','MF','MS','NI','PA','PE','PM','PR','PY','SR','SV','TT','UY','VC','VE','VG']
south=set(south)

diz=dict()
for i in data.keys(): #users

    if i not in bad: #filter out those with too high radius of gyration
        for j in range(len(data[i])):
            year=data[i][j][1]
            cond2=diz.get(year,'e')
            if cond2=='e':
                diz[year]={}
            c=data[i][j][0]
            if c in south:
                cond=diz[year].get(c,'e')
                if cond=='e':
                    diz[year][c]=set()
                    
                if i not in diz[year][c]:
                    diz[year][c].add(i) #for each year, save list of users appearing in each country
        
for year in diz:
    for c in diz[year]:
        print c, len(diz[year][c])
