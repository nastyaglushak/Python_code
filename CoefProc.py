import numpy as np
from matplotlib import pyplot as plt
from array import *

from IndTHRProcFun import CountChCalc, THRSort

delta=2.93
Ukal1=1200
Ukal2=800
dU=Ukal1-Ukal2
THRstep=1

data=[]
datan=[]

datay=[]
datayn=[]

datax=[]

coef=[]
deltacomamp=[]

for i in range (0,256/THRstep):
    datax.append(THRstep*i)

with open ("/home/glushak/Documents/chipdata/ChipSensor0106_1",'r') as f:
    for line in f.readlines():
        data.extend(line.rstrip().split(','))


with open ("/home/glushak/Documents/chipdata/ChipSensor0106_2",'r') as f:
    for line in f.readlines():
        datan.extend(line.rstrip().split(','))

for i in range (1,len(data)):
    datay.append(float(data[i]))
    datayn.append(float(datan[i]))


datay=np.array(datay).reshape (-1, 100)
datay=datay.transpose()

datayn=np.array(datayn).reshape (-1, 100)
datayn=datayn.transpose()

datachip_analysis, datachip_global=CountChCalc(datax, datay)

datachipn_analysis, datachip_globaln=CountChCalc(datax, datayn)


for i in range(0, len(datachip_analysis)):
    coef.append(delta*abs(datachip_analysis[i]-datachipn_analysis[i])/dU)


for i in range (0, len(datachipn_analysis)):
    deltacomamp.append(round((Ukal2*coef[i]-delta*datachipn_analysis[i]),2))

datacoefbin, datacoefhist=THRSort(coef, 256)
dataoffsetbin, datacoffsethist=THRSort(deltacomamp, 256)


fig,(ch1,ch2)=plt.subplots(1,2)
ch1.set_title ("Gain factor Histogram", fontsize=24)
ch1.bar ((datacoefbin[1:]+datacoefbin[:-1])/2.,datacoefhist, width=0.001) 
ch1.set_xlabel("Gain factor")
ch1.set_ylabel("Counts")
ch1.minorticks_on()
ch1.grid(which='minor', 
        color = 'k', 
        linestyle = ':')
ch1.grid(True)

ch2.set_title ("Offset Histogram", fontsize=24)
ch2.bar ((dataoffsetbin[1:]+dataoffsetbin[:-1])/2.,datacoffsethist, width=1) 
ch2.set_xlabel("Uoffset (mB)")
ch2.set_ylabel("Counts")
ch2.minorticks_on()
ch2.grid(which='minor', 
        color = 'k', 
        linestyle = ':')
ch2.grid(True)

plt.show()
