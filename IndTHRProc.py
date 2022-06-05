import numpy as np
from matplotlib import pyplot as plt
from array import *

from IndTHRProcFun import CountChCalc, THRSort, rolling_window

data=[]
datan=[]
datan2=[]
datay=[]
datayn=[]
datayn2=[]
datax=[]

for i in range (0,256):
    datax.append(i)

with open ("/home/glushak/Documents/chipdata/ChipData3105_5",'r') as f:
    for line in f.readlines():
        data.extend(line.rstrip().split(','))

with open ("/home/glushak/Documents/chipdata/ChipData3105_6",'r') as f:
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


print(datachip_analysis)
print("-------------")
print(datachipn_analysis)


databin, datahist=THRSort(datachip_analysis)
databinn, datahistn=THRSort(datachipn_analysis)

#Correct Algorithm

thrrange=[]
datarange=[]
dataint=[]

for i in range (0, 255): thrrange.append(i)
thrwindow=rolling_window(np.array(thrrange), 32)

for i in range (0, len(thrwindow)): datarange.append(0)

for i in range (0,len(thrwindow)):
    for k in range(0, len(datachip_analysis)):
        if (thrwindow[i][0]<=datachip_analysis[k]<=thrwindow[i][31]):datarange[i]+=1
print("DataRange",datarange, max(datarange))

for i in range(0, len(datarange)):
    if datarange[i]==max(datarange):
        dataint.append(i)
print("DataInt",dataint)


datathrav=thrwindow[dataint[0]][0]

print("DataTHR",datathrav,thrwindow[dataint[0]][0],thrwindow[dataint[len(dataint)-1]][31])

datarange_an=[]
for i in range(0, len(datachip_analysis)):
    if (thrwindow[dataint[0]][0]<=datachip_analysis[i]<=thrwindow[dataint[len(dataint)-1]][31]):
        datarange_an.append(datachip_analysis[i])

deltaTHR=[]
for i in range(0, len(datachip_analysis)):
    if (datathrav<datachip_analysis[i]<thrwindow[dataint[len(dataint)-1]][31]):
        deltaTHR.append(((-datathrav+datachip_analysis[i])))
    elif (datachip_analysis[i]>thrwindow[dataint[len(dataint)-1]][31]):
        deltaTHR.append(63)
    else:
        deltaTHR.append(0)
print("DeltaTHR",deltaTHR, len(deltaTHR))

#Make histograms
fig,(ch1,ch2)=plt.subplots(1,2)
ch1.set_title ("THR Old Histogram", fontsize=24)
ch1.bar ((databin[1:]+databin[:-1])/2.,datahist, width=0.5) 
ch1.set_xlim([0,256])
ch1.set_xlabel("THR")
ch1.set_ylabel("Counts")
ch1.minorticks_on()
ch1.grid(which='minor', 
        color = 'k', 
        linestyle = ':')
ch1.grid(True)

ch2.set_title ("THR New Histogram", fontsize=24)
ch2.bar ((databinn[1:]+databinn[:-1])/2.,datahistn, width=0.5) 
ch2.set_xlim([0,256])
ch2.set_xlabel("THR")
ch2.set_ylabel("Counts")
ch2.minorticks_on()
ch2.grid(which='minor', 
        color = 'k', 
        linestyle = ':')
ch2.grid(True)

plt.show()
