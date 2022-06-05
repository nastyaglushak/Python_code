import math
import numpy as np
from matplotlib import pyplot as plt

from IndTHRProcFun import CountChCalc, THRSort, CountCharPrint, THRHistPrint, CountCharPrint2x, DetectorChar

data=[]
datay=[]
datax=[]

data2=[]
datay2=[]
data3=[]
datay3=[]
data4=[]
datay4=[]

with open ("/home/glushak/Documents/chipdata/ChipDataAccum",'r') as f:
    for line in f.readlines():
        data.extend(line.rstrip().split(','))

for i in range (1,len(data)):
    datay.append(float(data[i]))


datay=np.array(datay).reshape (-1, 100)

datay=datay.transpose()

step=256/len(datay[0])

for i in range (0,len(datay[0])):
    datax.append(step*i)


with open ("/home/glushak/Documents/chipdata/ChipDataAccum2",'r') as f:
    for line in f.readlines():
        data2.extend(line.rstrip().split(','))

for i in range (1,len(data2)):
    datay2.append(float(data2[i]))

datay2=np.array(datay2).reshape (-1, 100)
datay2=datay2.transpose()

with open ("/home/glushak/Documents/chipdata/ChipSensor7",'r') as f:
    for line in f.readlines():
        data3.extend(line.rstrip().split(','))

for i in range (1,len(data3)):
    datay3.append(float(data3[i]))

datay3=np.array(datay3).reshape (-1, 100)
datay3=datay3.transpose()

with open ("/home/glushak/Documents/chipdata/ChipSensor34",'r') as f:
    for line in f.readlines():
        data4.extend(line.rstrip().split(','))

for i in range (1,len(data4)):
    datay4.append(float(data4[i]))

datay4=np.array(datay4).reshape (-1, 100)
datay4=datay4.transpose()

######For Many Characteristics
CountCharPrint2x(datax, datay, datay2)

DetectorChar(datax, datay)

####For Single Characteristics
CountCharPrint(datax, datay, 50)

datachip_analysis, datachip_global=CountChCalc(datax, datay)

print(datachip_analysis)
print("-------------")

databin, datahist=THRSort(datachip_analysis, 256)

THRHistPrint(databin, datahist)