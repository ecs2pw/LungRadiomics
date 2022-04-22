import pandas as pd
import datetime as dt
import numpy as np
from scipy.stats import t

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

#Put data into ITVdata and RITVdata
PTVdata={}
RPTVdata={}
for k in keys:
    X,y=[],[]
    for p in patients:
        X+=d[p]
        add=list(PTV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add]
        y+=add
    PTVdata[k]=(X,y)

    X,y=[],[]
    for p in patients:
        X+=d[p]
        add=list(Random_PTV[p].iloc[k])[1:]
        add=[float(i)/float(1) for i in add]
        y+=add
    RPTVdata[k]=(X,y)
    
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
        p=2*(1-t.cdf(abs(tStar),df=len(X)))
        print(len(X))
        results.append((PTV[patients[0]]["Unnamed: 0"][k], p))
    return results


PTVresults=slopeNotZero(PTVdata)
RPTVresults=slopeNotZero(RPTVdata)

combinedResults=[(PTVresults[i][0],PTVresults[i][1],RPTVresults[i][1]) for i in range(len(PTVresults))]
combinedResults.sort(key=lambda x: -x[1])

df=len(X)-1

for i in combinedResults:
    print(i[0],i[1],i[2])

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
plt.xlabel(r"R_PTV p ($\beta$=0)")
plt.ylabel(r"PTV p ($\beta$=0)")
plt.title("PTV vs RPTV Trend Significance")
plt.plot([0,1],[0.05,0.05],'r')
plt.show()

