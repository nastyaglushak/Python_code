import numpy as np
from matplotlib import pyplot as plt
from array import *

from IndTHRProcFun import CountChCalc, THRSort, rolling_window, THRsortSmall

data=[]
datan=[]
datan2=[]
datay=[]
datayn=[]
datayn2=[]
datax=[]

for i in range (0,32):
    datax.append(8*i)

with open ("/home/glushak/Documents/chipdata/ChipSensorTHRAll11",'r') as f:
    for line in f.readlines():
        data.extend(line.rstrip().split(','))

with open ("/home/glushak/Documents/chipdata/ChipSensorTHRAll12",'r') as f:
    for line in f.readlines():
        datan.extend(line.rstrip().split(','))

# with open ("/home/glushak/Documents/chipdata/ChipSensorAllTHR3",'r') as f:
#     for line in f.readlines():
#         datan2.extend(line.rstrip().split(','))

for i in range (1,len(data)):
    datay.append(float(data[i]))
    datayn.append(float(datan[i]))
    #datayn2.append(float(datan2[i]))

datay=np.array(datay).reshape (-1, 100)
datay=datay.transpose()

datayn=np.array(datayn).reshape (-1, 100)
datayn=datayn.transpose()

#datayn2=np.array(datayn2).reshape (-1, 100)
#datayn2=datayn2.transpose()

datachip_analysis, datachip_global=CountChCalc(datax, datay)
datachipn_analysis, datachip_globaln=CountChCalc(datax, datayn)
#datachipn_analysis2, datachip_globaln2=CountChCalc(datax, datayn2)

print(datachip_analysis)
print("-------------")
print(datachipn_analysis)

delta=[]
#delta2=[]

# for i in range (0, 96):
#     delta.append(datachip_analysis[i]-datachipn_analysis[i])
#     #delta2.append(datachip_analysis[i]-datachipn_analysis2[i])

# print("----------------")
# print(delta)

# with open ("dataout.txt", "w") as file:
#     file.write("Number"+" "+"Zero"+" "+"Average"+" "+"Max"+" "+"Delta"+" "+ "Delta2"+"\n")
#     for ind in range(0, 96):
#         file.write(str(ind)+" "+str(datachip_analysis[ind])+" "+str(datachipn_analysis[ind])+" "+str(delta[ind])+" "+"\n")

datachip_range=THRSort(datachip_analysis)
datachip_range_fornewdata=THRSort(datachipn_analysis)

datasmall_range=THRsortSmall(datachipn_analysis, 112,119)
print("DataSmall",datasmall_range)

#Correct Algorithm

thrrange=[]
datarange=[]
dataint=[]

for i in range (0, 255): thrrange.append(i)
thrwindow=rolling_window(np.array(thrrange), 33)
for i in range (0, len(thrwindow)): datarange.append(0)

for i in range (0,len(thrwindow)):
    for k in range(0, len(datachip_analysis)):
        if (thrwindow[i][0]<=datachip_analysis[k]<=thrwindow[i][32]):datarange[i]+=1
print("DataRange",datarange)

for i in range(0, len(datarange)):
    if datarange[i]==max(datarange):
        dataint.append(i)
print("DataInt",dataint)

if (len(dataint)==1):
    datathrav=(-thrwindow[dataint[0]][0]+thrwindow[dataint[0]][32])/2+thrwindow[dataint[0]][0]
else:
    datathrav=(-thrwindow[dataint[0]][0]+thrwindow[dataint[len(dataint)-1]][32])/2+thrwindow[dataint[0]][0]
print("DataTHR",datathrav,thrwindow[dataint[0]][0],thrwindow[dataint[len(dataint)-1]][32])

datarange_an=[]
for i in range(0, len(datachip_analysis)):
    if (thrwindow[dataint[0]][0]<=datachip_analysis[i]<=thrwindow[dataint[len(dataint)-1]][32]):
        datarange_an.append(datachip_analysis[i])

deltaTHR=[]
for i in range(0, len(datarange_an)):
    if (datarange_an[i]<datathrav):
        deltaTHR.append(2*(((datathrav-datarange_an[i]))))
    elif (datarange_an[i]>datathrav):
        deltaTHR.append(2*(((-datathrav+datarange_an[i]))))
    else:
        deltaTHR.append(0)
print("DeltaTHR",deltaTHR)


#Make histograms
bins = np.arange(0, 255, 8)
fig,(ch1,ch2)=plt.subplots(1,2)

ch1.bar(bins,datachip_range,width=8)
ch1.set_title ("THR Old Histogram", fontsize=24)
ch1.set_xlabel("Limits")
ch1.set_ylabel("Counts")
ch1.minorticks_on()
ch1.grid(which='minor', 
        color = 'k', 
        linestyle = ':')
ch1.grid(True)

ch2.bar(bins,datachip_range_fornewdata,width=8)
ch2.set_title ("THR New Histogram", fontsize=24)
ch2.set_xlabel("Limits")
ch2.set_ylabel("Counts")
ch2.minorticks_on()
ch2.grid(which='minor', 
        color = 'k', 
        linestyle = ':')
ch2.grid(True)
plt.show()

#np.savetxt('datasensor.txt',datachip_global,fmt='%.1f',delimiter='\t', header='Value THR')