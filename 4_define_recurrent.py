from __future__ import division
import pandas
import pickle
import pprint
import gpxpy.geo
import matplotlib.pyplot as plt
import numpy as np
import math
from itertools import groupby
from collections import defaultdict
import matplotlib as mpl
import matplotlib.cm as cm
from collections import Counter
from operator import itemgetter


pkl_file = open('moreve2dist.pkl','rb')
traj = pickle.load(pkl_file)
pkl_file.close()


diz=set()
escape=dict()
for i in traj.keys(): #user
    c0=traj[i][0][1] #first country in trajectory
    t0=traj[i][0][2] #first timestamp in trajectory
    for j in range(len(traj[i])): #tweets
        cf=traj[i][j][1]
        tf=traj[i][j][2]

        if cf!=c0: #if in new country
            if c0=='VE': #if first country was Venezuela
                if i not in diz: #I want only one entry per user
                    escape[i]=tf #save time of first exit from Venezuela
                    diz.add(i) #add user in the dict
                    break #pass to next user

output = open('escape.pkl','wb')
pickle.dump(escape, output)
output.close()

timeout=dict() #I want to measure how much time each user spends abroad
for i in escape.keys(): #user

    timeout[i]=0
    tesc=escape[i] #time of first exit
    for j in range(len(traj[i])): #tweets

        if j==len(traj[i])-1:
            break
        else:            
            t0=traj[i][j][2] #time
            c0=traj[i][j][1] #country
            cf=traj[i][j+1][1] #next point timestamp
            tf=traj[i][j+1][2] #next point country

            if tf>=tesc: #watch only after first exit
                if c0!='VE': #if abroad
                    timeout[i]+=tf-t0 #sum time spent abroad

recurrent=set()
for i in timeout.keys():
    if timeout[i]>0:
        deltat=traj[i][-1][2]-escape[i]
        ratio=timeout[i]/deltat
        if ratio<0.5: #I define users spending less then 50% of their time they as recurrent migrants
            recurrent.add(i)

output = open('recurrent.pkl','wb')
pickle.dump(recurrent, output)
output.close()
