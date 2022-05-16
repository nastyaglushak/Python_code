import numpy as np
from matplotlib import pyplot as plt
from array import *

def CountChCalc(datax, datay):
    datachip_one=[]
    datachip_global=[]

    for l in range (6, 12):
        l=l+1
        datachip_one=[]
        for j in range (0, 8*l):
            #seach 50% of counts
            for i in range (0, len(datay[j])):
                if (datay[j][i]>50):
                    data_max50=datay[j][i]
                    datathrmax=datax[i]
                    if (i==31):
                        data_min50=datay[j][i]
                        datathrmin=datax[i]
                    else:
                        data_min50=datay[j][i+1]
                        datathrmin=datax[i+1]
                    data_ind=i
            data50=float((data_max50-data_min50)/2+data_min50)
            if (data_ind==31):
                datathr=datax[data_ind]
            else:
                datathr=datathrmin+(-datathrmin+datathrmax)/2
            #fit
            for k in range (0,2):#8/2-1 iterations
                k=k+1
                if (data50<50):
                    data_min50=data50
                    datathrmin=datathr
                    data50=float((data_max50-data_min50)/2+data_min50)
                    datathr=datathrmin+(-datathrmin+datathrmax)/2
                else:
                    data_max50=data50
                    datathrmax=datathr
                    data50=float((data_max50-data_min50)/2+data_min50)
                    datathr=datathrmin+(-datathrmin+datathrmax)/2
            datachip_one.append(datathr)

    print("THRwithoutCorrect",datachip_one)
    datachip_global=np.around(np.array(datachip_one).reshape(-1,16),decimals=1)


    datachip_analysis=datachip_one
    return (datachip_analysis, datachip_global)

def THRSort(datachip_analysis):
    datachip_range=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range (0, len(datachip_analysis)):
        if (0<=datachip_analysis[i]<=7): datachip_range[0]+=1
        if (8<=datachip_analysis[i]<=15): datachip_range[1]+=1
        if (16<=datachip_analysis[i]<=23): datachip_range[2]+=1
        if (24<=datachip_analysis[i]<=31): datachip_range[3]+=1
        if (32<=datachip_analysis[i]<=39): datachip_range[4]+=1
        if (40<=datachip_analysis[i]<=47): datachip_range[5]+=1
        if (48<=datachip_analysis[i]<=55): datachip_range[6]+=1
        if (56<=datachip_analysis[i]<=63): datachip_range[7]+=1
        if (64<=datachip_analysis[i]<=71): datachip_range[8]+=1
        if (72<=datachip_analysis[i]<=79): datachip_range[9]+=1

        if (80<=datachip_analysis[i]<=87): datachip_range[10]+=1
        if (88<=datachip_analysis[i]<=95): datachip_range[11]+=1
        if (96<=datachip_analysis[i]<=103): datachip_range[12]+=1
        if (104<=datachip_analysis[i]<=111): datachip_range[13]+=1
        if (112<=datachip_analysis[i]<=119): datachip_range[14]+=1
        if (120<=datachip_analysis[i]<=127): datachip_range[15]+=1
        if (128<=datachip_analysis[i]<=135): datachip_range[16]+=1
        if (136<=datachip_analysis[i]<=143): datachip_range[17]+=1
        if (144<=datachip_analysis[i]<=151): datachip_range[18]+=1
        if (152<=datachip_analysis[i]<=159): datachip_range[19]+=1

        if (160<=datachip_analysis[i]<=167): datachip_range[20]+=1
        if (168<=datachip_analysis[i]<=175): datachip_range[21]+=1
        if (176<=datachip_analysis[i]<=183): datachip_range[22]+=1
        if (184<=datachip_analysis[i]<=191): datachip_range[23]+=1
        if (192<=datachip_analysis[i]<=199): datachip_range[24]+=1
        if (200<=datachip_analysis[i]<=207): datachip_range[25]+=1
        if (208<=datachip_analysis[i]<=215): datachip_range[26]+=1
        if (216<=datachip_analysis[i]<=223): datachip_range[27]+=1
        if (224<=datachip_analysis[i]<=231): datachip_range[28]+=1
        if (232<=datachip_analysis[i]<=239): datachip_range[29]+=1

        if (240<=datachip_analysis[i]<=247): datachip_range[30]+=1
        if (248<=datachip_analysis[i]<=255): datachip_range[31]+=1
    return(datachip_range)

def THRsortSmall(data_analysis, THR_start, THR_finish):
    data_range=[]
    for i in range(0,4):
        data_range.append(0)
    
    for i in range (0, len(data_analysis)):
        if (THR_start<=data_analysis[i]<=THR_start+1):data_range[0]+=1
        if (THR_start+2<=data_analysis[i]<=THR_start+3):data_range[1]+=1
        if (THR_start+4<=data_analysis[i]<=THR_start+5):data_range[2]+=1
        if (THR_start+6<=data_analysis[i]<=THR_start+7):data_range[3]+=1
    return(data_range)

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)