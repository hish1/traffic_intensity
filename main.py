from PyQt6 import uic, QtWidgets, QtWebEngineWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
import io
import sys
import folium
import pandas as pd
import qt.helperUi
from metrics import getData

def startUi(aqua, metric, file, metricFile):
    # m = folium.Map()
    m = getData(aqua, metric, file, metricFile)

    QtWidgets.QMainWindow.__init__(self)
    
    app = QtWidgets.QApplication(sys.argv)
    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(m.get_root().render())
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec())

def maindata(aqua, metric):
    
    global metricFile
    global file 
    
    if aqua == 0:
        file = 'D:\ii\уч еба\вкр\трафик\data\Tsugaru 02.07.2016.txt'
    elif aqua == 1:
        file = 'D:\\ii\\уч еба\\вкр\\трафик\\data\\25.02.2016.csv'
    else:
        file = 'D:\ii\уч еба\вкр\трафик\data\Tsugaru 02.07.2016.txt'

    if metric == 0:
        metricFile = 'D:\ii\уч еба\вкр\трафик\data\Sangar stream.txt'
    elif metric == 1:
        metricFile = ['D:\ii\уч еба\вкр\трафик\data\Sangar top.txt', 'D:\ii\уч еба\вкр\трафик\data\Sangar bottom.txt']

    startUi(aqua, metric, file, metricFile)

if __name__ == '__main__':
    maindata(0, 0)