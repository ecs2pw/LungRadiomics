import pandas as pd
import datetime as dt
import numpy as np
from scipy.stats import t

FilePath="/nv/vol141/phys_nrf/Emery/dataset/"

dates=pd.read_csv(FilePath+"Dates.csv")
patients=list(dates.columns)
blacklist=["DA","MK","MJ","BB"]
blacklist.append("CT")
blacklist.append("BJ")
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

#Put data into ITVdata and RITVdata
ITVdata={}
RITVdata={}
for k in keys:
    X,y=[],[]
    for p in patients:
        add=list(ITV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add]
        if not len(d[p]) == len(add):
            print("Patient",p,"has mis-matched lengths in ITV!")
            continue
        X+=d[p]
        y+=add
    ITVdata[k]=(X,y)

    X,y=[],[]
    for p in patients:
        add=list(Random_ITV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add]
        if not len(d[p]) == len(add):
            print("Patient",p,"has mis-matched lengths in R_ITV!")
            continue
        X+=d[p]
        y+=add
    RITVdata[k]=(X,y)
    
def slopeNotZero(data):
    results=[]
    for k in data:
        X=data[k][0]
        y=data[k][1]
        if not len(X)==len(y):
            print("X and y different lengths!")
            continue
        fit=np.polyfit(X, y, 1)
        p=np.poly1d(fit)

        b1=fit[0]
        Beta=0
        MSE=sum([(y[point]-p(X[point]))**2 for point in range(len(X))])/len(X)
        Xbar=sum(X)/len(X)
        idk=sum([(x-Xbar)**2 for x in X])
        tStar=(b1-Beta)/(MSE/idk)**0.5
        #print(ITV[patients[0]]["Unnamed: 0"][k],tStar)
        p=2*(1-t.cdf(abs(tStar),df=len(X)))
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
		results.append((ITV[patients[0]]["Unnamed: 0"][k], p, fit[0],m_Std))
		#print(fit[0],fit[1],y_Variance**0.5)
	return results


#ITVresults=slopeNotZero(ITVdata)
#RITVresults=slopeNotZero(RITVdata)
ITVresults=slopeStats(ITVdata)
RITVresults=slopeStats(RITVdata)

combinedResults=[(ITVresults[i][0],ITVresults[i][1],RITVresults[i][1]) for i in range(len(ITVresults))]
combinedResults.sort(key=lambda x: -x[1])

#df=len(X)-1

for i in range(len(ITVresults)):
	m_diff = abs(ITVresults[i][2]-RITVresults[i][2])
	m_StD = (ITVresults[i][3]**2+RITVresults[i][3]**3)**0.5
	print(i,2*(1-t.cdf(abs(m_diff)/m_StD,df=66)))

firstOrder = [i for i in combinedResults if "firstorder" in i[0]]
glcm = [i for i in combinedResults if "glcm" in i[0]]
glrlm = [i for i in combinedResults if "glrlm" in i[0]]
glszm = [i for i in combinedResults if "glszm" in i[0]]
gldm = [i for i in combinedResults if "gldm" in i[0]]
ngtdm = [i for i in combinedResults if "gldm" in i[0]]
import matplotlib.pyplot as plt
for j in [firstOrder, glcm, glrlm, glszm, gldm, ngtdm]:
    plt.scatter([i[2] for i in j], [i[1] for i in j])
plt.legend(["firstOrder",'glcm','glrlm','glszm','gldm','ngtdm'])
#plt.scatter([i[2] for i in combinedResults],[i[1] for i in combinedResults])
plt.xlabel(r"R_ITV p ($\beta$=0)")
plt.ylabel(r"ITV p ($\beta$=0)")
plt.title("ITV vs RITV Trend Significance")
plt.plot([0,1],[0.05,0.05],'r')
plt.show()

