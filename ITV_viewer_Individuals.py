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

ITVdata={}
RITVdata={}
colors=['b','g','r','c','m','y','k','orange']
c=0
for k in keys:
    if c==0:
        fig, axis = plt.subplots(3,3)
    col=0
    for p in patients:
        #X+=d[p]
        #Normalize to Pre, might want to change this
        y=list(ITV[p].iloc[k])[1:]
        y=[float(i)/float(1) for i in y] #/float(add[0])
        axis[c%3][c//3].scatter(d[p],y,s=2,color=colors[col])
        fit=np.polyfit(d[p],y,1)
        poly=np.poly1d(fit)
        axis[c%3][c//3].plot(d[p],poly(d[p]),linestyle='-',color=colors[col],linewidth=1)
        col+=1
    col=0
    for p in patients:
        y=list(Random_ITV[p].iloc[k])[1:]
        y=[float(i)/float(1) for i in y]
        #y+=add
        axis[c%3][c//3].scatter(d[p],y,marker="+",s=20,color=colors[col])
        fit=np.polyfit(d[p],y,1)
        poly=np.poly1d(fit)
        axis[c%3][c//3].plot(d[p],poly(d[p]),linestyle='--',color=colors[col],linewidth=1)
        col+=1
    
    axis[c%3][c//3].set_title(ITV[patients[0]]["Unnamed: 0"][i], fontsize=6)
    c+=1

    if c==9:
        #axis[2][2].legend(["ITV","R_ITV"],bbox_to_anchor=(1.3,3.8),loc='best')
        c=0
plt.show()
