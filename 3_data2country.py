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
from collections import defaultdict


## define users' trajectories at country level

data=pandas.read_csv('/home/mattia/Desktop/Venezuela1/res_time.csv','r', delimiter=' ', \
                    header=None, names=['uid','created_at','coordinates','country_code'], skiprows=1, index_col=None, skipinitialspace=True,\
                    squeeze=False)

data = data.sort_values('created_at')
data = data.drop_duplicates(['uid','created_at'])

from collections import Counter

def more(x):  #dataframe row as argument
    paesi=[]
    c=Counter(x['country_code'])
    print c
    if len(c)>1:
        return True
    else: return False

data = data.groupby('uid').filter(lambda x: more(x)) #drop those who appear in only one country

print data.head()

data["created_at"] = data["created_at"].apply(lambda t: datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S'))

data["created_at"] = data["created_at"].apply(lambda t: calendar.timegm(t.timetuple()))

data.set_index('uid', inplace=True)

traj=defaultdict(list)

def traject(x):
    user=x.name
    for i in range(len(x)):
        pais=x['country_code'].values[i]
        tiempo=x['created_at'].values[i]
        traj[user].append((pais,tiempo))
    
data.groupby('uid').apply(lambda x: traject(x))

print len(data), 'n tweets'

print len(data.groupby('uid')), 'n users'

output = open('moreve2country.pkl','wb')
pickle.dump(traj, output)
output.close()
