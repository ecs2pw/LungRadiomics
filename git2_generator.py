import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

FilePath="/nv/vol141/phys_nrf/Emery/dataset/"

dates=pd.read_csv(FilePath+"Dates.csv")
patients=list(dates.columns)
#TODO find out why last pre_negative is missing
#patients.remove("CT")
patients.remove("DA")
#Looks like some of this data might be bad
patients.remove("BJ")
patients.remove("MJ")

d={p:[dt.datetime.strptime(i,"%m/%d/%y") for i in dates[p] 
      if type(i)==type("")] for p in patients}
d={p:[(d[p][0]-i).days for i in d[p]] for p in d}


ITV={p:pd.read_csv(FilePath+p+"/PTV.csv") for p in patients}
PTV={p:pd.read_csv(FilePath+p+"/PTV.csv") for p in patients}
Random_ITV={p:pd.read_csv(FilePath+p+"/R_PTV.csv") for p in patients}
Random_PTV={p:pd.read_csv(FilePath+p+"/R_PTV.csv") for p in patients}

keys=[]
for i in ITV[patients[0]].index:
    try:
        val=float(ITV[patients[0]]["Pre"][i])
        keys.append(i)
    except:
        continue


ITVdata={}
RITVdata={}
for k in keys:
    #print(ITV[patients[0]]["Unnamed: 0"][k])
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
#square=3
key = keys[20]
for offset in range(0,510,10):
    plt.figure()
    fig, axis = plt.subplots(1, 1)
    axis.scatter(ITVdata[key][0],ITVdata[key][1], s=2, c='b')
    fit=np.polyfit(ITVdata[key][0], ITVdata[key][1], 1)
    p=np.poly1d(fit)
    axis.plot(ITVdata[key][0], p(ITVdata[key][0]), "b", linewidth=1)
    axis.scatter(RITVdata[key][0],RITVdata[key][1], s=2, c='r')
    fit=np.polyfit(RITVdata[key][0], RITVdata[key][1], 1)
    p=np.poly1d(fit)
    axis.plot(RITVdata[key][0], p(RITVdata[key][0]), "r", linewidth=1)
    axis.set_title(ITV[patients[0]]["Unnamed: 0"][key], fontsize=12)
    axis.legend(["PTV","R_PTV","PTV","R_PTV"],loc='upper right')
    c+=1
    plt.title(offset)
    plt.savefig("gif2/"+str(offset)+".png")
#plt.show()
