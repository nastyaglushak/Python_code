import math
import numpy as np
from matplotlib import pyplot as plt

data=[]
datay=[]
datax=[]

data2=[]
datay2=[]
data3=[]
datay3=[]
data4=[]
datay4=[]

with open ("/home/glushak/Documents/chipdata/ChipSensorTHRAll5",'r') as f:
    for line in f.readlines():
        data.extend(line.rstrip().split(','))

for i in range (1,len(data)):
    datay.append(float(data[i]))


for i in range (0,32):
    datax.append(8*i)

datay=np.array(datay).reshape (-1, 100)

datay=datay.transpose()

with open ("/home/glushak/Documents/chipdata/ChipSensorTHRAll6",'r') as f:
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

for i in range (0,12):
    print(i)
    k=8*i
    plt.rcParams["figure.figsize"]=(35,20)
    fig,ch=plt.subplots(2,4)
    fig.suptitle("Chip"+str(k/8+1), fontsize=24)
    ch[0,0].plot(datax, datay[0+k],datax, datay2[0+k], '--')
    ch[0,0].set_title('Channel1', fontsize=16)
    ch[0,0].grid()
    ch[0,0].set_xlabel("Limits")
    ch[0,0].set_ylabel("Counts")
    ch[0,1].plot(datax, datay[1+k],datax, datay2[1+k],'--')
    ch[0,1].set_title('Channel2', fontsize=16)
    ch[0,1].grid()
    ch[0,1].set_xlabel("Limits")
    ch[0,1].set_ylabel("Counts")

    ch[0,2].plot(datax, datay[2+k],datax, datay2[2+k], '--')
    ch[0,2].set_title('Channel3', fontsize=16)
    ch[0,2].grid()
    ch[0,2].set_xlabel("Limits")
    ch[0,2].set_ylabel("Counts")
    ch[0,3].plot(datax, datay[3+k],datax,datay2[3+k],'--')
    ch[0,3].set_title('Channel4', fontsize=16)
    ch[0,3].grid()
    ch[0,3].set_xlabel("Limits")
    ch[0,3].set_ylabel("Counts")

    ch[1,0].plot(datax, datay[4+k],datax, datay2[4+k], '--')
    ch[1,0].set_title('Channel5', fontsize=16)
    ch[1,0].grid()
    ch[1,0].set_xlabel("Limits")
    ch[1,0].set_ylabel("Counts")
    ch[1,1].plot(datax, datay[5+k],datax, datay2[5+k], '--')
    ch[1,1].set_title('Channel6', fontsize=16)
    ch[1,1].grid()
    ch[1,1].set_xlabel("Limits")
    ch[1,1].set_ylabel("Counts")

    ch[1,2].plot(datax, datay[6+k],datax, datay2[6+k],'--')
    ch[1,2].set_title('Channel7', fontsize=16)
    ch[1,2].grid()
    ch[1,2].set_xlabel("Limits")
    ch[1,2].set_ylabel("Counts")
    ch[1,3].plot(datax, datay[7+k],datax,datay2[7+k],'--')
    ch[1,3].set_title('Channel8', fontsize=16)
    ch[1,3].grid()
    ch[1,3].set_xlabel("Limits")
    ch[1,3].set_ylabel("Counts")

    plt.savefig('ChipSensor_{0}.png'.format(k/8+1))
    #plt.show()



#Detector Characteristic
fig2=plt.figure()
ax=fig2.add_subplot(111)
#ax.plot(datax, datay[97], datax, datay2[97],'--', datax, datay3[97],'-.',datax, datay4[97],'-*',linewidth=4.0)
ax.plot(datax, datay[1],linewidth=4.0)
ax.set_title ("Detector Counter Characteristic", fontsize=24)
ax.set_xlabel("Limits", fontsize=16)
ax.set_ylabel("Counts", fontsize=24)

ax.grid(True)
ax.minorticks_on()
ax.grid(which='major',
        color = 'k', 
        linewidth = 2)
ax.grid(which='minor', 
        color = 'k', 
        linestyle = ':')
ax.legend(['0V', '100V', '200V', '300V'])
#fig2.savefig('ChipSensorCh.png')
#plt.show()