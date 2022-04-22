import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

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
for i in ITV[patients[0]].index:
    try:
        val=float(ITV[patients[0]]["Pre"][i])
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
        X+=d[p]
        #Normalize to Pre, might want to change this
        add=list(ITV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add] #/float(add[0])
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


c=0
square=3
for i in keys:
    if c==0:
        fig, axis = plt.subplots(square, square)
        
    axis[c%square][c//square].scatter(ITVdata[i][0],ITVdata[i][1], s=2, c='b')
    fit=np.polyfit(ITVdata[i][0], ITVdata[i][1], 1)
    p=np.poly1d(fit)
    axis[c%square][c//square].plot(ITVdata[i][0], p(ITVdata[i][0]), "b", linewidth=1)
    axis[c%square][c//square].scatter(RITVdata[i][0],RITVdata[i][1], s=2, c='r')
    fit=np.polyfit(RITVdata[i][0], RITVdata[i][1], 1)
    p=np.poly1d(fit)
    axis[c%square][c//square].plot(RITVdata[i][0], p(RITVdata[i][0]), "r", linewidth=1)
    axis[c%square][c//square].set_title(ITV[patients[0]]["Unnamed: 0"][i], fontsize=6)
    c+=1

    if c==square**2:
        #axis[2][2].legend(["ITV","R_ITV","ITV","R_ITV"],bbox_to_anchor=(1.3,3.8),loc='best')
        c=0
plt.show()
