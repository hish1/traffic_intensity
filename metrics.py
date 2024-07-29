import folium, time, json, random, sys, folium
import pandas as pd
from glob import glob
from mac import mainmac as mac
from PyQt6 import QtWidgets, QtWebEngineWidgets
from shapely.geometry import LineString, Polygon, Point
from shapely.ops import split
import shapely as sh


bords = [[13998500, 14125500], [13966301, 14004272], [13494919, 13537354], 
         [12863754, 12899185], [13188357, 13193198], [13291400, 13301700]]
colors = ['red', 'green', 'navy', 'deeppink', 'black', 'darkorange',
          'purple', 'maroon', 'magenta', 'olive', 'lawngreen']

def getStreams(file, metric):
    f = open(file+metric, 'r')
    line = f.readline()[:-1]
    array = []
    while line != '':
        l = line.split(', ')

        for j in range(6):
            l[j] = float(l[j])

        array.append(l)
        line = f.readline()[:-1]
    return array

def getarrays(file, metric):
    arrays = []
    for m in metric:
        f = open(file+m, 'r')
        line = f.readline()[:-1]
        array = []
        while line != '':
            l = line.split(', ')
            arr = []
            arr.append(float(l[0]))
            arr.append(float(l[1]))
            array.append(arr)

            line = f.readline()[:-1]
        arrays.append(array)
    return arrays

def get_num(num):
    dig = str(num).split('.')
    if len(dig[1])<5:
        for i in range(abs(len(dig[1])-5)):
            dig[1] += '0'
    ten = 1
    for g in dig[1]:
        ten*=10
    num = int(dig[0])*ten+int(dig[1])

    return num

def count(num):
    n = str(num)[-5:]
    num = str(num)[:-5]+'.'+n

    return float(num)

def count_dec(num):
    llat = str(num).split('.')
    if len(llat[1])>5:
        llat[1] = llat[1][:5]

        num = float(llat[0]+'.'+llat[1])

    return num

def check_borders(arrays, route, metric):
    
    for ar in arrays:
        for i in range(len(ar))-1:
            a = LineString([(ar[i][0], ar[i][1]), (ar[i+1][0], ar[i+1][1])])
            for j in range(len(route)-1):
                b = LineString([(route[j][0], route[j][1]), (route[j+1][0], route[j+1][1])])
                if a.intersects(b):
                    route[j+1][0] = ar[i+1][0]
                    route[j+1][1] = ar[i+1][1]

def loc_bordered(arrays, loc, id):
    # array = []
    # for ar in arrays:
    #     a = []
    #     for i in range(len(ar)):
    #         a.append((ar[i][0], ar[i][1]))
    #     array.append(ar)
    # a = LineString(array[0])
    # b = LineString(array[1])
    # intersection = sh.intersection_all([a, b])

    # border = []
    # if intersection==intersection:
    #     if intersection.length>0:
    #         for i in intersection:
    #             border.append(intersection.y)
    #     else:
    #         border.append(count_dec(intersection.y))
    
    d = []
    ll = len(loc)-1
    for ar in arrays:
        for i in range(len(ar)-1):
            a = LineString([(ar[i][0], ar[i][1]), (ar[i+1][0], ar[i+1][1])])
            j = 0
            # for j in range(len(route)-1):
            while j<len(loc)-1:
                if loc[j][1]<count(bords[id][0]):
                    d.append(j)
                    d.append(ll-j)
                elif loc[j][1]>count(bords[id][1]):
                    d.append(j)
                    d.append(ll-j)
                else:
                    b = LineString([(loc[j][0], loc[j][1]), (loc[ll-j][0], loc[ll-j][1])])
                    if a.intersects(b):
                        if ar==arrays[0]:
                            n = min(ar[i][0], ar[i+1][0])
                            loc[j][0] = n-0.00030
                        else:
                            n = max(ar[i][0], ar[i+1][0])
                            loc[ll-j][0] = n+0.00030
                j += 1
    
    l = []
    for i in range(len(loc)):
        if i not in d:
            l.append(loc[i])

    return l


def getData(m, file, metric=0, metricFile=''):
    
    if metric==0:
        return m
    else:
        flag = [True, False]
        start = time.time()

        l = {}
        location = []
        files = glob(file[0]+'*.xlsx')[:-2]
        files = files[:1]

        if flag[1]:
                
            for f in files:

                df = pd.read_excel(f, usecols=[1, 2 , 3, 4, 5, 7])
                data = df.values
                nans = []

                for i in range(data.shape[0]):
                    
                    flag = True
                    for j in range(1, 6):

                        if data[i][0]!=data[i][0]:
                            nans.append(i)
                            break
                        else:
                            d = int(data[i][0])

                            if data[i][0] not in l.keys():
                                l[d] = {
                                    1: [],
                                    2: [],
                                    3: [],
                                    4: [],
                                    5: []
                                }

                            f = j==1 or j==2
                            length = len(l[d][j])
                            if length==0 or (data[i][j] != l[d][j][length-1] or j!=1):
                                a = data[i][j]
                                if j==5:
                                    a = str(a.time())
                                    
                                l[d][j].append(a)
                            elif j==1:
                                if data[i][j+1] != l[d][j+1][length-1]:
                                    l[d][j].append(data[i][j])
                                else:
                                    break
                            else:
                                break

                print(nans)
                print(time.time()-start)

            # with open(file[0]+"days.json", "w") as write_file:
            #     json.dump(l, write_file)
            with open(file[0]+"day2.json", "w") as write_file:
                json.dump(l, write_file)

            exit()
        
        if flag[1]:
            
            with open(file[0]+"day2.json", "r") as f:
                l = json.load(f)

            ar = []
            for id in l:
                if len(l[id]['1'])<10:
                    ar.append(id)
            for id in ar:
                del l[id]

            with open(file[0]+"day2.json", "w") as write_file:
                json.dump(l, write_file)

            print(time.time()-start)
            exit()

        # df = pd.read_excel(file[0]+'marine.xlsx', usecols=[0, 6])
        # data = df.values

        # for id, length in data:
        #     if id in l.keys():
        #         l[id][6] = length

        # print(time.time()-start)

        c = 0
        location = []

        with open(file[0]+"day2.json", "r") as f:
            l = json.load(f)

        rand = []
        for i in range(10):
            a = random.choice(list(l.keys()))
            while a in rand:
                a = random.choice(list(l.keys()))
            rand.append(a)

        if flag[1]:

            for j in range(bords[file[1]][0], bords[file[1]][1], 10):
                dic = {}

                lat = 0
                lon = 0
                i = 0
                for r in rand:
                    if j > 14082000:
                        a = 1

                    if r not in dic.keys():
                        k = 0
                    else:
                        k = dic[r]

                    a = l[r]
                    num = get_num(a['1'][k])

                    while num<j:
                        # lon += a['1'][k]
                        lat += a['2'][k]
                        i+=1

                        k+=1
                        if k<=len(a['1'])-1:
                            num = get_num(a['1'][k])
                        else: 
                            break
                    
                    dic[r] = k

                if lat!=0:
                    # lon /= i
                    lat /= i

                    # lon = count_dec(lon)
                    lat = count_dec(lat)

                    lon = str(j)[-5:]
                    j = str(j)[:-5]
                    lon = float(j+'.'+lon)

                    loc = [lat, lon]
                    
                    if loc not in location:
                        location.append(loc)

            print(f'пути: {time.time()-start}')
            # print(location)

            with open(file[0]+"route.json", "w") as write_file:
                json.dump(location, write_file)

            exit()
            
        if flag[1]:
            with open(file[0]+"route.json", "r") as f:
                route = json.load(f)
                
            arrays = getarrays(file[0], metricFile)
            d = []
            for ar in arrays:

                i = 0
                n, v = 0, 140
                for j in range(len(ar)-1):
                    while i<len(route) and route[i][1]<ar[j][1]:
                        b = arrays[0][len(arrays[0])-1][1]
                        if  route[i][1]>b:
                            d.append(i)
                        else:
                            if ar==arrays[0]:
                                if route[i][0]>=ar[j][0]:
                                    # if ar[j][<0]=ar[j+1][0]:
                                    v = min(ar[j][0], ar[j+1][0])
                                    route[i][0] = v-0.00050
                                    # else:
                                    #     route[i+1][0] = ar[j+1][0]-0.00050
                            else:
                                # a = route[i][0]
                                # b = route[i+1][0]
                                # c = ar[j][0]
                                # d = ar[j+1][0]

                                if route[i][0]<=ar[j][0]:
                                # if route[i][0]<=n:
                                    n = max(ar[j][0], ar[j+1][0])
                                    route[i][0] = n+0.00050
                        i += 1
            a = []
            for i in range(len(route)-15):
                if i not in d:
                    a.append(route[i])
            route = a
            # route[len(route)-1][0] = arrays[1][len(arrays[1])-1][0]

            print(f'границы: {time.time()-start}')
            with open(file[0]+"route.json", "w") as write_file:
                json.dump(route, write_file)

            exit()

        # другие суда
        if metric == 1:
            
            if flag[1]:
                for r in rand:
                    a=[]
                    for i in range(len(l[r]['1'])):
                        a.append([l[r]['2'][i], l[r]['1'][i]])
                
                    c+=1
                    f = folium.PolyLine(locations=a, color=colors[c], weight=5, smooth_factor=10).add_to(m)
                    print(r+' '+colors[c])

            with open(file[0]+"route.json", "r") as f:
                location = json.load(f)

            f = folium.PolyLine(locations=location, color=colors[c], weight=7, smooth_factor=10).add_to(m)
            # print(r+' '+colors[c])
            # c+=1

        # течения
        elif metric == 2:
            array = getStreams(file[0], metricFile)
            for i in range(len(array)-1):
                loc = [[array[i][0], array[i][2]], [array[i][0], array[i][3]],
                       [array[i][0], array[i][2]], [array[i][1], array[i][2]],
                       [array[i][1], array[i][2]], [array[i][1], array[i][3]],
                       [array[i][1], array[i][3]], [array[i][0], array[i][3]]]
                folium.Polygon(locations=loc, color='blue', weight=3).add_to(m)

            with open(file[0]+"route.json", "r") as f:
                location = json.load(f)
            f = folium.PolyLine(locations=location, color=colors[c], weight=7, smooth_factor=10).add_to(m)

        # препятствия
        elif metric == 3:

            arrays = getarrays(file[0], metricFile)
            for a in arrays:
                if a!=[]:
                    f = folium.PolyLine(locations=a, color='yellow', weight=5, smooth_factor=10).add_to(m)
                    
            with open(file[0]+"route.json", "r") as f:
                location = json.load(f)
            f = folium.PolyLine(locations=location, color=colors[c], weight=7, smooth_factor=10).add_to(m)

        elif metric == 4:
            array = mac.mainmac(file[0])
            arrays = getarrays(file[0], metricFile)

            locGreen = []
            locOrange = []
            locRed = []

            with open(file[0]+"getIntencitylocGreen.json", "r") as f:
                locGreen = json.load(f)
            with open(file[0]+"getIntencitylocOrange.json", "r") as f:
                locOrange = json.load(f)
            with open(file[0]+"getIntencitylocRed.json", "r") as f:
                locRed = json.load(f)

            if locGreen!=[]:
                locGreen = loc_bordered(arrays, locGreen, file[1])
                with open(file[0]+"getMetricVelocitylocGreen.json", "w") as write_file:
                    json.dump(locGreen, write_file)
            if locOrange!=[]:
                locOrange = loc_bordered(arrays, locOrange, file[1])
                with open(file[0]+"getMetricVelocitylocOrange.json", "w") as write_file:
                    json.dump(locOrange, write_file)
            if locRed!=[]:
                locRed = loc_bordered(arrays, locRed, file[1])
                with open(file[0]+"getMetricVelocitylocRed.json", "w") as write_file:
                    json.dump(locRed, write_file)
            # exit()

            if locGreen!=[]:
                folium.Polygon(locations=locGreen, weight=0, fill_color='green', fill_opacity=0.3).add_to(m)
            if locOrange!=[]:
                folium.Polygon(locations=locOrange, weight=0, fill_color='darkorange', fill_opacity=0.5).add_to(m)
            if locRed!=[]:
                folium.Polygon(locations=locRed, weight=0, fill_color='red', fill_opacity=0.5).add_to(m)
            
            print(f'полигоны 4: {time.time()-start}')

        elif metric == 5:
            array = mac.mainmac(file[0], 2)
            arrays = getarrays(file[0], metricFile)
            
            locGreen = []
            locOrange = []
            locRed = []

            with open(file[0]+"getMetricVelocitylocGreen.json", "r") as f:
                locGreen = json.load(f)
            with open(file[0]+"getMetricVelocitylocOrange.json", "r") as f:
                locOrange = json.load(f)
            with open(file[0]+"getMetricVelocitylocRed.json", "r") as f:
                locRed = json.load(f)
            
            if locGreen!=[]:
                locGreen = loc_bordered(arrays, locGreen, file[1])
                with open(file[0]+"getMetricVelocitylocGreen.json", "w") as write_file:
                    json.dump(locGreen, write_file)
            if locOrange!=[]:
                locOrange = loc_bordered(arrays, locOrange, file[1])
                with open(file[0]+"getMetricVelocitylocOrange.json", "w") as write_file:
                    json.dump(locOrange, write_file)
            if locRed!=[]:
                locRed = loc_bordered(arrays, locRed, file[1])
                with open(file[0]+"getMetricVelocitylocRed.json", "w") as write_file:
                    json.dump(locRed, write_file)
            # exit()

            if locGreen!=[]:
                folium.Polygon(locations=locGreen, weight=0, fill_color='green', fill_opacity=0.3).add_to(m)
            if locOrange!=[]:
                folium.Polygon(locations=locOrange, weight=0, fill_color='darkorange', fill_opacity=0.5).add_to(m)
            if locRed!=[]:
                folium.Polygon(locations=locRed, weight=0, fill_color='red', fill_opacity=0.5).add_to(m)
            
            print(f'полигоны 5: {time.time()-start}')

        elif metric == 6:
            array = mac.mainmac(file[0], 3)
            arrays = getarrays(file[0], metricFile)
            
            locGreen = []
            locOrange = []
            locRed = []

            with open(file[0]+"getMetricSizelocGreen.json", "r") as f:
                locGreen = json.load(f)
            with open(file[0]+"getMetricSizelocOrange.json", "r") as f:
                locOrange = json.load(f)
            with open(file[0]+"getMetricSizelocRed.json", "r") as f:
                locRed = json.load(f)

            if locGreen!=[]:
                locGreen = loc_bordered(arrays, locGreen, file[1])
                with open(file[0]+"getMetricVelocitylocGreen.json", "w") as write_file:
                    json.dump(locGreen, write_file)
            if locOrange!=[]:
                locOrange = loc_bordered(arrays, locOrange, file[1])
                with open(file[0]+"getMetricVelocitylocOrange.json", "w") as write_file:
                    json.dump(locOrange, write_file)
            if locRed!=[]:
                locRed = loc_bordered(arrays, locRed, file[1])
                with open(file[0]+"getMetricVelocitylocRed.json", "w") as write_file:
                    json.dump(locRed, write_file)
            # exit()

            if locGreen!=[]:
                folium.Polygon(locations=locGreen, weight=0, fill_color='green', fill_opacity=0.3).add_to(m)
            if locOrange!=[]:
                folium.Polygon(locations=locOrange, weight=0, fill_color='darkorange', fill_opacity=0.5).add_to(m)
            if locRed!=[]:
                folium.Polygon(locations=locRed, weight=0, fill_color='red', fill_opacity=0.5).add_to(m)
            
            print(f'полигоны 6: {time.time()-start}')

        return m


if __name__ == '__main__':
    
    m = folium.Map(location=[43.1045 , 131.90306], zoom_start = 14)
    getData(m, ['D:\\ii\\уч еба\\вкр\\трафик\\data\\Vladivostok\\', 1], 5, ['VladivostokTop.txt', 'VladivostokBottom.txt'])
    
    app = QtWidgets.QApplication(sys.argv)
    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(m.get_root().render())
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec())