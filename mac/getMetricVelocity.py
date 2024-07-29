import numpy as num
from math import floor
import json, time

def make_json(array, file):
    with open(file+"getMetricVelocity.json", "w") as write_file:
        json.dump(array, write_file)

    exit()

def read_json(file):
    array = 0
    with open(file+"getMetricVelocity.json", "r") as f:
        array = json.load(f)

    return array

def make_number(num):
    n = str(num).split('.')
    if len(n[1])>4:
        d = n[1][:5]
        num = float(n[0]+'.'+d)

    return num

def figures(axesLat, array):
    loc = []
    g = []
    for i in range(len(axesLat)):
        g = []
        lat = make_number(axesLat[i])
        for l in array:
            if l[1]==lat:
                g.append(l[0])
        if g != []:
            m = max(g)
            loc.append([m, lat])
    
    for i in range(len(axesLat)-1, -1, -1):
        g = []
        lat = make_number(axesLat[i])
        for l in array:
            if l[1]==lat:
                g.append(l[0])
        if g != []:
            m = min(g)
            loc.append([m, lat])

    return loc

def mirror(axesLat, array):
    l = len(axesLat)-1

    for i in range(l+1):
        axesLat[i] = make_number(axesLat[i])
    
    for i in range(len(array)):
        ind = axesLat.index(array[i][1])
        array[i][1] = axesLat[l-ind]
        
    return array

def getTrafficInPointIntencityOptimizedMetricVelocity(traceMatrix,  minLon, stepLon, maxLon, minLat, stepLat, maxLat, file):
    f = [True, False]
    start = time.time()

    earthRadius  = 6500000.00000
    mn = len(traceMatrix)

    axesLon = []
    for i in num.arange(minLon, maxLon, stepLon):
        axesLon.append(i)
    axesLat = []
    for i in num.arange(minLat, maxLat, stepLat):
        axesLat.append(i)

    axesLonSize = len(axesLon)
    axesLatSize = len(axesLat)


    if f[1]:

        trafficIntensity = num.zeros((axesLatSize+1, axesLonSize+1)).tolist()

        isInCellMatrix = num.zeros((10000, 3)).tolist()
        isInCellMatrixRowNumber = 0

        for i in range(1, mn):
            moveLatMeters = traceMatrix[i][4]/10.0 * 1852.0 / 3600.0 * num.cos(traceMatrix[i][5]/180.0*num.pi) * traceMatrix[i][6] * 60.0
            moveLonMeters = traceMatrix[i][4]/10.0 * 1852.0 / 3600.0 * num.sin(traceMatrix[i][5]/180.0*num.pi) * traceMatrix[i][6] * 60.0
            moveLat = 180 * moveLatMeters / earthRadius / num.pi 
            moveLon = 180 * moveLonMeters / (earthRadius * num.pi * num.cos(minLat/180.0*num.pi)) 
            currLat =  traceMatrix[i][2] + moveLat
            currLon =  traceMatrix[i][3] + moveLon

            if currLat >= minLat and currLat <= maxLat and currLon >= minLon and currLon <= maxLon:
                iLat = axesLatSize - round((currLat - minLat) / (maxLat - minLat) * (axesLatSize - 1))  
                iLon = round((currLon - minLon) / (maxLon - minLon) * (axesLonSize - 1) + 1)
                
                # is ship in cell matrix 
                isInCellMatrixFlag = 0
                for j in range(1, isInCellMatrixRowNumber):
                    if traceMatrix[i][0] == isInCellMatrix[j][0] and iLat == isInCellMatrix[j][1] and iLon == isInCellMatrix[j][2]:
                        isInCellMatrixFlag = 1
                        break
            
                # if ship NOT in matrix
                if isInCellMatrixFlag == 0:
                    # 1 per 10 knots
                    trafficIntensity[iLat][iLon] += floor(traceMatrix[i][4]/100) + 1; 
                    isInCellMatrixRowNumber += 1
                    isInCellMatrix[isInCellMatrixRowNumber][0] = traceMatrix[i][0]
                    isInCellMatrix[isInCellMatrixRowNumber][1] = iLat
                    isInCellMatrix[isInCellMatrixRowNumber][2] = iLon
            
        for i in range(len(trafficIntensity)):
            for j in range(len(trafficIntensity[i])):
                trafficIntensity[i][j] = int(trafficIntensity[i][j])+1
                if trafficIntensity[i][j]>1:
                    print(f'{trafficIntensity[i][j]}, [{i}, {j}]')

        print(f'Metric Velocity: {time.time()-start}')
        make_json(trafficIntensity, file)

    if f[1]:
        trafficIntensity = read_json(file)
        result = num.zeros((axesLatSize+1, axesLonSize+1)).tolist()
        for i in range(len(trafficIntensity)):
            lat = make_number(minLat+stepLat*i)
            for j in range(len(trafficIntensity[i])):
                lon = make_number(minLon+stepLon*j)
                t = trafficIntensity[i][j]
                result[i][j] = [lon, lat, t]
        print(f'Metric Velocity with weight: {time.time()-start}')
        make_json(result, file)

    if f[1]:
        array = read_json(file)
        
        locGreen = []
        locOrange = []
        locRed = []

        for i in range(len(array)):
            for j in range(len(array[i])):
                if array[i][j][2]>10:
                    locRed.append([array[i][j][0], array[i][j][1]])
                elif array[i][j][2]>2:
                    locOrange.append([array[i][j][0], array[i][j][1]])
                else:
                    locGreen.append([array[i][j][0], array[i][j][1]])

        locGreen = figures(axesLat, locGreen)
        locOrange = figures(axesLat, locOrange)
        locRed = figures(axesLat, locRed)

        locGreen = mirror(axesLat, locGreen)
        locOrange = mirror(axesLat, locOrange)
        locRed = mirror(axesLat, locRed)
        
        with open(file+"getMetricVelocitylocGreen.json", "w") as write_file:
            json.dump(locGreen, write_file)
        with open(file+"getMetricVelocitylocOrange.json", "w") as write_file:
            json.dump(locOrange, write_file)
        with open(file+"getMetricVelocitylocRed.json", "w") as write_file:
            json.dump(locRed, write_file)

        print(f'Metric Velocity colored: {time.time()-start}')
        exit()


    trafficIntensity = read_json(file)
    return trafficIntensity