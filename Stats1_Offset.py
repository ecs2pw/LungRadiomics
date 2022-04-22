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


#Values for offset
for offset in range(0,510,10):
	#continue
	ITVresults=slopeNotZero(strip(offset)[0])
	RITVresults=slopeNotZero(strip(offset)[1])

	combinedResults=[(ITVresults[i][0],ITVresults[i][1],RITVresults[i][1]) for i in range(len(ITVresults))]
	combinedResults.sort(key=lambda x: -x[1])

	tempX=[i for i in X if i>=offset]
	df=len(tempX)-1

	print(str(offset)+":",len(tempX))

	firstOrder = [i for i in combinedResults if "firstorder" in i[0]]
	glcm = [i for i in combinedResults if "glcm" in i[0]]
	glrlm = [i for i in combinedResults if "glrlm" in i[0]]
	glszm = [i for i in combinedResults if "glszm" in i[0]]
	gldm = [i for i in combinedResults if "gldm" in i[0]]
	ngtdm = [i for i in combinedResults if "gldm" in i[0]]

	plt.figure()
	for j in [firstOrder, glcm, glrlm, glszm, gldm, ngtdm]:
		plt.scatter([i[2] for i in j], [i[1] for i in j])
	plt.legend(["firstOrder",'glcm','glrlm','glszm','gldm','ngtdm'], loc="upper right")
	#plt.scatter([i[2] for i in combinedResults],[i[1] for i in combinedResults])
	plt.xlabel(r"R_ITV p ($\beta$=0)")  
	plt.ylabel(r"ITV p ($\beta$=0)")
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.title(offset)
	plt.plot([0,1],[0.05,0.05],'r')
	#plt.show()
	plt.savefig("gif/"+str(offset)+".png")



#Create gif
images=[i for i in os.listdir("gif") if not i.endswith(".gif")]
images.sort(key=lambda x: int(x[:-4]))
print(images)
with imageio.get_writer("gif/gif.gif", mode='I') as writer:
	for imageName in images:
		image=imageio.imread("gif/"+imageName)
		writer.append_data(image)
		writer.append_data(image)
	for i in range(10):
		writer.append_data(image)

