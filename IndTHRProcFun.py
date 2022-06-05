import numpy as np
from matplotlib import pyplot as plt
from array import *
import math

THRstart = 50
THRmax = 256


def CountChCalc(datax, datay):
    datachip_one = []
    datachip_global = []

    #Code for finding a reference for each channel
    delta = 0.01
 
    for k in range(0, 95):
        ref = 0
        count = 0
        for i in range(0, THRstart):
            if (datay[k][i+1] < datay[k][i]):
                if ((datay[k][i]-datay[k][i+2])/datay[k][i] < delta):
                    ref += datay[k][i]
                    count += 1
                    #print(round(datay[k][i]))
        #print(ref, count)

    dataref = datay[0][THRstart]
    step = 256/len(datay[0])

    dataxstep = int(math.log(step, 2))
    print(dataxstep)

    for p in range(1, 12):
        p = p+1
        datachip_one = []
        for j in range(0, 8*p):
            # seach 50% of counts
            for i in range(THRstart, len(datay[j])):
                # print(i,j,datay[j][i])
                if (datay[j][i] > 0.5*dataref):
                    data_max50 = datay[j][i]
                    datathrmax = datax[i]
                    if (i == THRmax-1):
                        data_min50 = datay[j][i]
                        datathrmin = datax[i]
                    else:
                        data_min50 = datay[j][i+1]
                        datathrmin = datax[i+1]
                    data_ind = i+1
            #print(p, data_ind, j, data_max50, data_min50)
            data50 = float((data_max50-data_min50)/2+data_min50)

            if (data_ind == THRmax-1):
                datathr = datax[data_ind]
            else:
                datathr = datathrmin+(-datathrmin+datathrmax)/2

            # fit
            for k in range(0, dataxstep):  # 8/2-1 iterations
                k = k+1
                if (data50 < 50):
                    data_min50 = data50
                    datathrmin = datathr
                    data50 = float((data_max50-data_min50)/2+data_min50)
                    datathr = datathrmin+(-datathrmin+datathrmax)/2
                else:
                    data_max50 = data50
                    datathrmax = datathr
                    data50 = float((data_max50-data_min50)/2+data_min50)
                    datathr = datathrmin+(-datathrmin+datathrmax)/2
            datachip_one.append(datathr)

    print("THRwithoutCorrect", datachip_one, len(datachip_one))
    # datachip_global=np.around(np.array(datachip_one).reshape(-1,16),decimals=1)

    datachip_analysis = datachip_one
    return (datachip_analysis, datachip_global)


def THRSort(dataIn, binNum):
    datachip_range = np.array(dataIn)
    databin = np.linspace(0, round(max(dataIn), 2), binNum)
    datahist = []
    for i in range(len(databin)-1):
        mask = (datachip_range >= databin[i]) & (datachip_range < databin[i+1])
        datahist.append(len(datachip_range[mask]))
    return databin, datahist


def THRsortSmall(data_analysis, THR_start, THR_finish):
    data_range = []
    for i in range(0, 4):
        data_range.append(0)

    for i in range(0, len(data_analysis)):
        if (THR_start <= data_analysis[i] <= THR_start+1):
            data_range[0] += 1
        if (THR_start+2 <= data_analysis[i] <= THR_start+3):
            data_range[1] += 1
        if (THR_start+4 <= data_analysis[i] <= THR_start+5):
            data_range[2] += 1
        if (THR_start+6 <= data_analysis[i] <= THR_start+7):
            data_range[3] += 1
    return(data_range)


def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def DataFileOut(dataIn1, dataIn2):
    with open("dataout.txt", "w") as file:
        file.write("Number"+" "+"Zero"+" "+"Average"+" " +
                   "Max"+" "+"Delta"+" " + "Delta2"+"\n")
        for ind in range(0, 96):
            file.write(
                str(ind)+" "+str(dataIn1[ind])+" "+str(dataIn2[ind])+"\n")


def CountCharPrint(datax, datay, THRref):
    for i in range(0, 12):
        print(i)
        k = 8*i
        plt.rcParams["figure.figsize"] = (35, 20)
        fig, ch = plt.subplots(2, 4)
        fig.suptitle("Chip"+str(k/8+1), fontsize=24)
        ch[0, 0].plot(datax[THRref:], datay[0+k][THRref:])
        ch[0, 0].set_title('Channel1', fontsize=16)
        ch[0, 0].grid()
        ch[0, 0].set_xlabel("Limits")
        ch[0, 0].set_ylabel("Counts")
        ch[0, 1].plot(datax[THRref:], datay[1+k][THRref:])
        ch[0, 1].set_title('Channel2', fontsize=16)
        ch[0, 1].grid()
        ch[0, 1].set_xlabel("Limits")
        ch[0, 1].set_ylabel("Counts")

        ch[0, 2].plot(datax[THRref:], datay[2+k][THRref:])
        ch[0, 2].set_title('Channel3', fontsize=16)
        ch[0, 2].grid()
        ch[0, 2].set_xlabel("Limits")
        ch[0, 2].set_ylabel("Counts")
        ch[0, 3].plot(datax[THRref:], datay[3+k][THRref:])
        ch[0, 3].set_title('Channel4', fontsize=16)
        ch[0, 3].grid()
        ch[0, 3].set_xlabel("Limits")
        ch[0, 3].set_ylabel("Counts")

        ch[1, 0].plot(datax[THRref:], datay[4+k][THRref:])
        ch[1, 0].set_title('Channel5', fontsize=16)
        ch[1, 0].grid()
        ch[1, 0].set_xlabel("Limits")
        ch[1, 0].set_ylabel("Counts")
        ch[1, 1].plot(datax[THRref:], datay[5+k][THRref:])
        ch[1, 1].set_title('Channel6', fontsize=16)
        ch[1, 1].grid()
        ch[1, 1].set_xlabel("Limits")
        ch[1, 1].set_ylabel("Counts")

        ch[1, 2].plot(datax[THRref:], datay[6+k][THRref:])
        ch[1, 2].set_title('Channel7', fontsize=16)
        ch[1, 2].grid()
        ch[1, 2].set_xlabel("Limits")
        ch[1, 2].set_ylabel("Counts")
        ch[1, 3].plot(datax[THRref:], datay[7+k][THRref:])
        ch[1, 3].set_title('Channel8', fontsize=16)
        ch[1, 3].grid()
        ch[1, 3].set_xlabel("Limits")
        ch[1, 3].set_ylabel("Counts")

        plt.savefig('DataProc_{0}.png'.format(k/8+1))
        #plt.show()

def CountCharPrint2x(datax, datay, datay2):
    for i in range (0,12):
        print(i)
        k=8*i
        plt.rcParams["figure.figsize"]=(35,20)
        fig,ch=plt.subplots(2,4)
        fig.suptitle("Chip"+str(k/8+1), fontsize=24)
        ch[0,0].plot(datax[50:], datay[0+k][50:],datax[50:], datay2[0+k][50:], '--')
        ch[0,0].set_title('Channel1', fontsize=16)
        ch[0,0].grid()
        ch[0,0].set_xlabel("Limits")
        ch[0,0].set_ylabel("Counts")
        ch[0,1].plot(datax[40:], datay[1+k][40:],datax[40:], datay2[1+k][40:],'--')
        ch[0,1].set_title('Channel2', fontsize=16)
        ch[0,1].grid()
        ch[0,1].set_xlabel("Limits")
        ch[0,1].set_ylabel("Counts")

        ch[0,2].plot(datax[40:], datay[2+k][40:],datax[40:], datay2[2+k][40:], '--')
        ch[0,2].set_title('Channel3', fontsize=16)
        ch[0,2].grid()
        ch[0,2].set_xlabel("Limits")
        ch[0,2].set_ylabel("Counts")
        ch[0,3].plot(datax[30:], datay[3+k][30:],datax[30:],datay2[3+k][30:],'--')
        ch[0,3].set_title('Channel4', fontsize=16)
        ch[0,3].grid()
        ch[0,3].set_xlabel("Limits")
        ch[0,3].set_ylabel("Counts")

        ch[1,0].plot(datax[30:], datay[4+k][30:],datax[30:], datay2[4+k][30:], '--')
        ch[1,0].set_title('Channel5', fontsize=16)
        ch[1,0].grid()
        ch[1,0].set_xlabel("Limits")
        ch[1,0].set_ylabel("Counts")
        ch[1,1].plot(datax[40:], datay[5+k][40:],datax[40:], datay2[5+k][40:], '--')
        ch[1,1].set_title('Channel6', fontsize=16)
        ch[1,1].grid()
        ch[1,1].set_xlabel("Limits")
        ch[1,1].set_ylabel("Counts")

        ch[1,2].plot(datax[40:], datay[6+k][40:],datax[40:], datay2[6+k][40:],'--')
        ch[1,2].set_title('Channel7', fontsize=16)
        ch[1,2].grid()
        ch[1,2].set_xlabel("Limits")
        ch[1,2].set_ylabel("Counts")
        ch[1,3].plot(datax[40:], datay[7+k][40:],datax[40:],datay2[7+k][40:],'--')
        ch[1,3].set_title('Channel8', fontsize=16)
        ch[1,3].grid()
        ch[1,3].set_xlabel("Limits")
        ch[1,3].set_ylabel("Counts")

        plt.savefig('ChipSensor_{0}.png'.format(k/8+1))
        #plt.show()

def THRHistPrint(databin, datahist):
    fig,(ch1)=plt.subplots(1,1)
    ch1.bar ((databin[1:]+databin[:-1])/2.,datahist, width=1) 
    ch1.set_title ("THR Histogram", fontsize=24)
    ch1.set_xlabel("Limits")
    ch1.set_xlim([0,256])
    ch1.set_ylabel("Counts")
    ch1.minorticks_on()
    ch1.grid(which='minor', 
        color = 'k', 
        linestyle = ':')
    ch1.grid(True)
    plt.show()

def DetectorChar(datax, datay):
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