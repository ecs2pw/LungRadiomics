import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

FilePath="/nv/vol141/phys_nrf/Emery/dataset/"
#I had written that CT has some missing data, not sure if that was fixed but they look alright now
#BJ data appears to be bad, I'm including them for now to avoid cherry-picking patients
#MK is missing some data
blacklist=["DA","MK","MJ"]
blacklist.append("BB")
dates=pd.read_csv(FilePath+"Dates.csv")
patients=list(dates.columns)
for i in blacklist:
    if i in patients:
        patients.remove(i)

volumes = pd.read_csv(FilePath+"newPatientList.csv")
vols = {p:[] for p in patients}
for i in range(len(volumes['Initials'])):
	if volumes['Initials'][i] in vols:
		for j in volumes['ITV Vols'][i].split():
			if j[-1]==',':
				vols[volumes['Initials'][i]].append(float(j[:-1]))
			else:
				vols[volumes['Initials'][i]].append(float(j))


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
        if len(vols[p]) == 0:
            continue
        add=float(ITV[p].iloc[k][1])
        X.append(vols[p][0])
        y.append(add)
    if not len(X)==len(y):
        print(p,"X and y different lengths")
        continue
    ITVdata[k]=(X,y)

    X,y=[],[]
    for p in patients:
        if (len(vols[p]) == 0):
            continue
        add=float(Random_ITV[p].iloc[k][1])
        y.append(add)
        X.append(vols[p][0])
    RITVdata[k]=(X,y)


c=0
square=3
fig_num=0
for i in keys:
    if c==0:
        fig, axis = plt.subplots(square, square)
        fig_num += 1
        
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
        plt.gcf().set_size_inches(15,10)
        plt.savefig("ITV_Vols/Fig_"+str(fig_num)+".png",dpi=200)
plt.gcf().set_size_inches(15,10)
plt.savefig("ITV_Vols/Fig_"+str(fig_num)+".png",dpi=200)
plt.show()
