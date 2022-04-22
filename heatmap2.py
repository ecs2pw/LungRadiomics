import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
from scipy.stats import linregress
import sys

ratio = float(sys.argv[1])


FilePath="/nv/vol141/phys_nrf/Emery/dataset/"
#I had written that CT has some missing data, not sure if that was fixed but they look alright now
#BJ data appears to be bad, I'm including them for now to avoid cherry-picking patients
#MK is missing some data
blacklist=["DA","MK","MJ","BB"]
dates=pd.read_csv(FilePath+"Dates.csv")
patients=list(dates.columns)
for i in blacklist:
    if i in patients:
        patients.remove(i)


d={p:[dt.datetime.strptime(i,"%m/%d/%y") for i in dates[p] 
      if type(i)==type("")] for p in patients}
d={p:[(d[p][0]-i).days for i in d[p]] for p in d}


ITV={p:pd.read_csv(FilePath+p+"/ITV.csv") for p in patients}
PTV={p:pd.read_csv(FilePath+p+"/PTV.csv") for p in patients}
Random_ITV={p:pd.read_csv(FilePath+p+"/R_ITV.csv") for p in patients}
Random_PTV={p:pd.read_csv(FilePath+p+"/R_PTV.csv") for p in patients}

keys=[]
for i in ITV[patients[-1]].index:
    try:
        val=float(ITV[patients[-1]]["Pre"][i])
        keys.append(i)
    except:
        continue
print("Examining",len(keys),"features.")
print("Patients:",len(patients))
print("Timesteps:",sum([len(d[p]) for p in patients]))

ITVdata={}
RITVdata={}
for k in keys:
    X,y=[],[]
    for p in patients:
        #X+=d[p]
        #Normalize to Pre, might want to change this
        add=list(ITV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add] #/float(add[0])
        #y+=add
        if not len(d[p]) == len(add):
            print("size mismatch, skipping")
            continue
        X+=d[p]
        y+=add
    if not len(X)==len(y):
        print(p,"X and y different lengths")
        continue
    ITVdata[k]=(X,y)

    X,y=[],[]
    for p in patients:
        X+=d[p]
        add=list(Random_ITV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add]
        y+=add
    RITVdata[k]=(X,y)

featureNames = {k:ITV[patients[0]]["Unnamed: 0"][k] for k in keys}
prefixes = ["diagnostics_Image-original","original_shape","original_firstorder","original_glcm","original_gldm","original_glrlm","original_glszm","original_ngtdm"]
data = {featureNames[k]: ITVdata[k][1] for k in keys}

for prefix in prefixes:
	r=[]
	for i in data:
		if not i.startswith(prefix):
			continue
		dat = []
		names = []
		for j in data:
			if not j.startswith(prefix):
				continue
			dat.append(linregress(data[i],data[j]).rvalue**2)
			names.append(j)
		r.append(dat)


	num = ratio*len(r)
	choices = []
	for n in range(int(num)):
		mins = [min(row) for row in r]
		ind = mins.index(min(mins))
		choices.append(names[ind])
		for row in r:
			del row[ind]
		del r[ind]
		del names[ind]
	print(prefix,choices)

plt.show()
