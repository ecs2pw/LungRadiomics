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
#patients.remove("BJ")
patients.remove("MK")

d={p:[dt.datetime.strptime(i,"%m/%d/%y") for i in dates[p] 
      if type(i)==type("")] for p in patients}
d={p:[(d[p][0]-i).days for i in d[p]] for p in d}


ITV={p:pd.read_csv(FilePath+p+"/ITV.csv") for p in patients}
PTV={p:pd.read_csv(FilePath+p+"/PTV.csv") for p in patients}
Random_ITV={p:pd.read_csv(FilePath+p+"/R_ITV.csv") for p in patients}
Random_PTV={p:pd.read_csv(FilePath+p+"/R_PTV.csv") for p in patients}

keys=[]
for i in PTV[patients[0]].index:
    try:
        val=float(PTV[patients[0]]["Pre"][i])
        keys.append(i)
    except:
        continue

PTVdata={}
RPTVdata={}
for k in keys:
    #print(ITV[patients[0]]["Unnamed: 0"][k])
    X,y=[],[]
    for p in patients:
        X+=d[p]
        #Normalize to Pre, might want to change this
        add=list(PTV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add] #/float(add[0])
        y+=add
    if not len(X)==len(y):
        print(p,"X and y different lengths")
        continue
    PTVdata[k]=(X,y)

    X,y=[],[]
    for p in patients:
        X+=d[p]
        add=list(Random_PTV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add]
        y+=add
    RPTVdata[k]=(X,y)


c=0
square=3
for i in keys:
    #try:
    #    val=float(ITV["Pre"][i])
    #except:
    #    print("Bad Key!")
    #    continue
    if c==0:
        #plt.figure()
        fig, axis = plt.subplots(square, square)
        
    axis[c%square][c//square].scatter(PTVdata[i][0],PTVdata[i][1], s=2, c='b')
    fit=np.polyfit(PTVdata[i][0], PTVdata[i][1], 1)
    p=np.poly1d(fit)
    axis[c%square][c//square].plot(PTVdata[i][0], p(PTVdata[i][0]), "b", linewidth=1)
    axis[c%square][c//square].scatter(RPTVdata[i][0],RPTVdata[i][1], s=2, c='r')
    fit=np.polyfit(RPTVdata[i][0], RPTVdata[i][1], 1)
    p=np.poly1d(fit)
    axis[c%square][c//square].plot(RPTVdata[i][0], p(RPTVdata[i][0]), "r", linewidth=1)
    #vals=[float(j) for j in ITV.iloc[i][1:]]
    #axis[c%4][c//4].plot(X, vals)
    #vals=[float(j) for j in PTV.iloc[i][1:]]
    #axis[c%4][c//4].plot(X, vals)
    #vals=[float(j) for j in Random_ITV.iloc[i][1:]]
    #axis[c%4][c//4].plot(X, vals)
    #vals=[float(j) for j in Random_PTV.iloc[i][1::]]
    #axis[c%4][c//4].plot(X, vals)
    axis[c%square][c//square].set_title(PTV[patients[0]]["Unnamed: 0"][i], fontsize=6)
    c+=1

    if c==square**2:
        axis[2][2].legend(["PTV","R_PTV","PTV","R_PTV"],bbox_to_anchor=(1.3,3.8),loc='best')
        c=0
plt.show()
