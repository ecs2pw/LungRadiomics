import pandas as pd
import datetime as dt
import numpy as np
from scipy.stats import t
import matplotlib.pyplot as plt
import os
import imageio

#Read in patient data

FilePath="/nv/vol141/phys_nrf/Emery/dataset/"

dates=pd.read_csv(FilePath+"Dates.csv")
patients=list(dates.columns)
blacklist=["DA","MK","MJ"]
for i in blacklist:
    if i in patients:
        patients.remove(i)
d={p:[dt.datetime.strptime(i,"%m/%d/%y") for i in dates[p] 
      if type(i)==type("")] for p in patients}
d={p:[(d[p][0]-i).days for i in d[p]] for p in d}

#offset=int(input("How many days would you like to cut off? "))

ITV={p:pd.read_csv(FilePath+p+"/ITV.csv") for p in patients}
PTV={p:pd.read_csv(FilePath+p+"/PTV.csv") for p in patients}
Random_ITV={p:pd.read_csv(FilePath+p+"/R_ITV.csv") for p in patients}
Random_PTV={p:pd.read_csv(FilePath+p+"/R_PTV.csv") for p in patients}

keys=[] #Keys are feature names
for i in ITV[patients[0]].index:
    try:
        val=float(ITV[patients[0]]["Pre"][i])
        keys.append(i)
    except:
        continue


#Put data into ITVdata and RITVdata
ITVdata={}
RITVdata={}
for k in keys:
    X,y=[],[]
    for p in patients:
        X+=d[p]
        add=list(ITV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add]
        y+=add
    ITVdata[k]=(X,y)

    X,y=[],[]
    for p in patients:
        X+=d[p]
        add=list(Random_ITV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add]
        y+=add
    RITVdata[k]=(X,y)

#Remove points prior to offset
def strip(offset, ITVdata=ITVdata, RITVdata=RITVdata, keys=keys):
	ITV,RITV = {},{}
	for k in keys:
		X,y=ITVdata[k]
		ITV[k]=([i for i in X if not i<offset], [y[i] for i in range(len(y)) if not X[i]<offset])
		X,y=RITVdata[k]
		RITV[k]=([i for i in X if not i<offset], [y[i] for i in range(len(y)) if not X[i]<offset])
	return ITV,RITV
    
def slopeNotZero(data):
    results=[]
    for k in data:
        X=data[k][0]
        y=data[k][1]
        fit=np.polyfit(X, y, 1)
        p=np.poly1d(fit)

        b1=fit[0]
        Beta=0
        MSE=sum([(y[point]-p(X[point]))**2 for point in range(len(X))])/len(X)
        Xbar=sum(X)/len(X)
        idk=sum([(x-Xbar)**2 for x in X])
        tStar=(b1-Beta)/(MSE/idk)**0.5
        #print(ITV[patients[0]]["Unnamed: 0"][k],tStar)
        p=2*(1-t.cdf(abs(tStar),df=len(X)-1))
        #print(len(X))
        results.append((ITV[patients[0]]["Unnamed: 0"][k], p))
    return results

def slopeStats(data):
	results=[]
	for k in data:
		X=data[k][0]
		y=data[k][1]
		if not len(X)==len(y):
			print("X and y different lengths!")
			continue
		fit=np.polyfit(X,y,1)
		p=np.poly1d(fit)
		Xbar = sum(X)/len(X)
		y_Variance=sum([(y[i]-p(X[i]))**2 for i in range(len(X))])/(len(X)-2)
		SSxx = sum([(X[i] - Xbar)**2 for i in range(len(X))])
		m_Std =  (y_Variance/SSxx)**0.5
		#print(k,fit[0],m_Std)
		p=2*(1-t.cdf(abs(fit[0]/m_Std), df=len(X)))
		results.append((ITV[patients[0]]["Unnamed: 0"][k], fit[0], m_Std))
		#print(fit[0],fit[1],y_Variance**0.5)
	return results




ITVresults=slopeStats(strip(0)[0])
RITVresults=slopeStats(strip(0)[1])

p={}
for i in range(len(ITVresults)):
	df=len(X)-1
	m_diff = abs(ITVresults[i][1]-RITVresults[i][1])
	m_StD = (ITVresults[i][2]**2+RITVresults[i][2]**3)**0.5
	p[i]=2*(1-t.cdf(abs(m_diff)/m_StD,df=df))
bestKeys=sorted(p.keys(), key=lambda x: p[x])
best=bestKeys[:5]
for i in bestKeys:
	print(i,p[i])


#Values for offset
bestStats={i:[] for i in best}
for offset in range(0,295,5):
	#continue
	ITVresults=slopeStats(strip(offset)[0])
	RITVresults=slopeStats(strip(offset)[1])

	p={}
	for b in best:
		df=len([j for j in X if j>=offset])-1
		m_diff = abs(ITVresults[b][1]-RITVresults[b][1])
		m_StD = (ITVresults[b][2]**2+RITVresults[b][2]**3)**0.5
		p=2*(1-t.cdf(abs(m_diff)/m_StD,df=df))
		bestStats[b].append(p)

	#combinedResults=[(ITVresults[i][0],ITVresults[i][1],RITVresults[i][1]) for i in range(len(ITVresults))]
	#combinedResults.sort(key=lambda x: -x[1])

	tempX=[i for i in X if i>=offset]
	#df=len(tempX)-1

	print(str(offset)+":",len(tempX))

for i in bestStats:
	plt.plot([i for i in range(0,295,5)],bestStats[i])
plt.legend([ITVresults[b][0] for b in bestStats])
plt.title("Power of feature slope difference over time")
plt.xlabel("Days before diagnosis")
plt.ylabel("p ($\Delta$$\\beta$=0)")
plt.show()



