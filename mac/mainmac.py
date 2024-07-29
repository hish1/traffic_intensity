import numpy as num 
from glob import glob
import matplotlib.pyplot as plt
# from mac import getIntencity, getMetricSize, getMetricVelocity
import getIntencity, getMetricSize, getMetricVelocity
import pandas as pd
import json, time

def read(file, i):
    if i==0:
        df = pd.read_excel(file+'17.11.2015.xlsx', usecols=[1, 2 , 3, 4, 5, 6, 7])
        data = df.values
    else:
        df = pd.read_excel(file+'marine.xlsx', usecols=[0, 6])
        data = df.values

    data = data.tolist()
    return data

def get_time(time):
    time = str(time)
    time = time.split(' ')[1].split(':')[:2]
    time = float(time[0]+'.'+time[1])

    return time

def make_json(file, i):
    data = read(file, i)

    if i==0:
        for i in range(len(data)):
            data[i][6] = get_time(data[i][6])
        
        with open(file+"traceMatrix.json", "w") as write_file:
            json.dump(data, write_file)
    else:
        with open(file+"sizeMatrix.json", "w") as write_file:
            json.dump(data, write_file)

    exit()

def read_json(i, file):
    l = 0
    
    if i==0:
        with open(file+"traceMatrix.json", "r") as f:
            l = json.load(f)
    else:
        with open(file+"sizeMatrix.json", "r") as f:
            l = json.load(f)

    return l


def mainmac(file, id=1):
    start = time.time()

    # make_json(file, 0)
    # make_json(file, 1)

    traceMatrix = read_json(0, file)

    earthRadius = 6500000.00000

    maxTraceMatrix = num.max(traceMatrix, 0)
    minTraceMatrix = num.min(traceMatrix, 0)
    maxLat = maxTraceMatrix[1]
    maxLon = maxTraceMatrix[2]
    minLat = minTraceMatrix[1]
    minLon = minTraceMatrix[2]

    # minLat = 40.5939
    # minLon = 139.5394
    # maxLat = 41.9911
    # maxLon = 141.8490

    stepMeters = 1000
    stepLat = abs(180 * stepMeters / earthRadius / num.pi)
    stepLon = abs(180 * stepMeters / (earthRadius * num.pi * num.cos(minLat/180*num.pi)))

    if (id==2):
        trafficIntensity_visual = getMetricVelocity.getTrafficInPointIntencityOptimizedMetricVelocity(traceMatrix,  minLon, stepLon, maxLon, minLat, stepLat, maxLat, file)
    elif (id==3):
        sizeMatrix = read_json(1, file)
        trafficIntensity_visual = getMetricSize.getTrafficInPointIntencityOptimizedMetricSize(traceMatrix,  minLon, stepLon, maxLon, minLat, stepLat, maxLat, sizeMatrix, file)
    else:
        trafficIntensity_visual = getIntencity.getTrafficInPointIntencityOptimized(traceMatrix,  minLon, stepLon, maxLon, minLat, stepLat, maxLat, file)

    return trafficIntensity_visual

if __name__ == '__main__':
    mainmac('D:\\ii\\уч еба\\вкр\\трафик\\data\\Nahodka\\', 3)