import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

FilePath="/nv/vol141/phys_nrf/Emery/dataset/"

badPatients=["LK", "BJ", "DA"]

VolData=pd.read_csv(FilePath+"newPatientList.csv")
initials=VolData["Initials"]
ITV_Vols=VolData["ITV Vols"]
PTV_Vols=VolData["PTV Vols"]
RITV_Vols=VolData["R_ITV Vols"]
RPTV_Vols=VolData["R_PTV Vols"]
for i in range(len(initials)):
    if not len(str(initials[i]))==2 or str(initials[i]) in badPatients:
        continue
    a=[float(x) for x in ITV_Vols[i].replace(",","").split()]
    b=[float(x) for x in PTV_Vols[i].replace(",","").split()]
    plt.plot([i/a[0] for i in a], color='r')
    plt.plot([i/b[0] for i in b], color='b')
plt.legend(["ITV Vols", "PTV Vols"])

plt.figure()
for i in range(len(initials)):
    if not len(str(initials[i]))==2:
        continue
    c=[float(x) for x in RITV_Vols[i].replace(",","").split()]
    d=[float(x) for x in RPTV_Vols[i].replace(",","").split()]
    plt.plot([i/c[0] for i in c], color='r')
    plt.plot([i/d[0] for i in d], color='b')
plt.legend(["R_ITV Vols", "R_PTV Vols"])
plt.show()





