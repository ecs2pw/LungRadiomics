import pandas as pd
import datetime as dt
import numpy as np
from scipy.stats import t
import pickle

FilePath="/nv/vol141/phys_nrf/Emery/dataset/"

dates=pd.read_csv(FilePath+"Dates.csv")
patients=list(dates.columns)
blacklist=["DA","MK","MJ","BB"]
blacklist.append("CT")
blacklist.append("BJ")
for i in blacklist:
    if i in patients:
        patients.remove(i)


#Read in dates
print("Reading timesteps")
d={p:[dt.datetime.strptime(i,"%m/%d/%y") for i in dates[p] 
      if type(i)==type("")] for p in patients}
d={p:[(d[p][0]-i).days for i in d[p]] for p in d}


#Read in data
print("Reading radiometric data")
ITV={p:pd.read_csv(FilePath+p+"/ITV.csv") for p in patients}
PTV={p:pd.read_csv(FilePath+p+"/PTV.csv") for p in patients}
Random_ITV={p:pd.read_csv(FilePath+p+"/R_ITV.csv") for p in patients}
Random_PTV={p:pd.read_csv(FilePath+p+"/R_PTV.csv") for p in patients}

#Determine valid keys
print("Finding valid features")
keys, names = [],{}
for i in ITV[patients[0]].index:
    try:
        val=float(ITV[patients[0]]["Pre"][i])
        keys.append(i)
        names[i]=ITV[patients[0]]["Unnamed: 0"][i]
    except:
        continue



#Put data into ITVdata and RITVdata
print("Processing data")
def process(dataset):
	outData = {}
	for k in keys:
		X,y = [],[]
		for p in patients:
			add = list(dataset[p].iloc[k])[1:]
			add = [float(i) for i in add]
			if not len(d[p]) == len(add):
				print("Patient",p,"has mis-matched lengths! (in process)")
				continue
			X += d[p]
			y += add
		outData[k] = (X,y)
	return outData

ITVdata = process(ITV)
RITVdata = process(Random_ITV)
PTVdata = process(PTV)
RPTVdata = process(Random_PTV)



def slopeStats(X, y):
#Taken from https://pages.mtu.edu/~fmorriso/cm3215/UncertaintySlopeInterceptOfLeastSquaresFit.pdf
	if not len(X)==len(y):
		print("X and y different lengths! (in slopeStats)")
		return
	if len(X) < 3:
		print("X has",len(X),"datapoints, need at least 3 for analysis!")
		return
	yBar, xBar = sum(y)/len(y), sum(X)/len(X)
	SS_yy, SS_xx = sum([(i - yBar)**2 for i in y]), sum([(i - xBar)**2 for i in X])
	SS_xy = sum([(X[i]-xBar)*(y[i]-yBar) for i in range(len(X))])

	mHat = SS_xy/SS_xx
	bHat = yBar - mHat*xBar
	SS_T, SS_E = SS_yy, sum([(bHat + mHat*X[i] - y[i])**2 for i in range(len(y))])
	df, n = len(X)-2, len(X)
	s_yx = (SS_E/df)**0.5
	s_m, s_b = s_yx/(SS_xx**0.5), s_yx*(1/n + xBar**2/SS_xx)**0.5
	SS_R = SS_T - SS_E
	if SS_E == 0:
		R2 = 1.0
	else:
		R2 = (SS_T-SS_E)/SS_T
	
	#fit=np.polyfit(X,y,1)
	#p=np.poly1d(fit)
	#Xbar = sum(X)/len(X)
	#y_Variance=sum([(y[i]-p(X[i]))**2 for i in range(len(X))])/(len(X)-2)
	#SSxx = sum([(X[i] - Xbar)**2 for i in range(len(X))])
	#m_Std =  (y_Variance/SSxx)**0.5
	#return (fit[0],mHat, m_Std,s_m)
	
	return (mHat, s_m, R2)


print("Fitting linear models")
ITV_fits, RITV_fits = {},{}
PTV_fits, RPTV_fits = {},{}
for k in ITVdata.keys():
	ITV_fits[names[k]] = slopeStats(ITVdata[k][0], ITVdata[k][1])
	RITV_fits[names[k]] = slopeStats(RITVdata[k][0], RITVdata[k][1])
	PTV_fits[names[k]] = slopeStats(PTVdata[k][0], PTVdata[k][1])
	RPTV_fits[names[k]] = slopeStats(RPTVdata[k][0], RPTVdata[k][1])
allData = {'ITV':ITV_fits, 'PTV':PTV_fits, "RITV":RITV_fits, "RPTV:":RPTV_fits}

print("Saving fits")
with open("TrendData.fit", 'wb') as file:
	pickle.dump(allData, file)

print("done.")


