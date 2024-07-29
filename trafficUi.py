from PyQt6 import uic, QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import sys, folium, time
from metrics import getData

# файлы акваторий
file = [
    'D:\\ii\\уч еба\\вкр\\трафик\\data\\Sangar\\', 'D:\\ii\\уч еба\\вкр\\трафик\\data\\Tokio\\',
    'D:\\ii\\уч еба\\вкр\\трафик\\data\\Osaka\\', 'D:\\ii\\уч еба\\вкр\\трафик\\data\\Pusan\\',
    'D:\\ii\\уч еба\\вкр\\трафик\\data\\Vladivostok\\', 'D:\\ii\\уч еба\\вкр\\трафик\\data\\Nahodka\\'
    ]
loc = [
    [[41.54369, 140.67444], 10], [[35.50367, 139.86969], 11], [[34.57612, 135.14969], 10],
    [[35.03623, 128.87169], 11], [[43.1045 , 131.90306], 14], [[42.7683, 132.96753], 12]
    ]

# файлы метрик
metric = {
    0: ['SangarStream.txt', ['SangarTop.txt', 'SangarBottom.txt']],
    1: ['TokioStream.txt', ['TokioTop.txt', 'TokioBottom.txt']],
    2: ['OsakaStream.txt', ['OsakaTop.txt', 'OsakaBottom.txt']],
    3: ['PusanStream.txt', ['PusanTop.txt', 'PusanBottom.txt']],
    4: ['VladivostokStream.txt', ['VladivostokTop.txt', 'VladivostokBottom.txt']],
    5: ['NahodkaStream.txt', ['NahodkaTop.txt', 'NahodkaBottom.txt']],
}

# названия кнопок
locs = ['Сангарский пролив', 'Токио', 'Осака', 'Пусан', 'Владивосток', 'Находка']
names = ['Нет', 'Количество судов', 'Течения', 'Географические препятствия (граница суши)', 'Интенсивность трафика (Ит)', 'Ит + скорость судов', 'Ит + размеры судов']


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        font = QtGui.QFont()
        font.setPointSize(12)

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("ТРАФИК")
        MainWindow.resize(1147, 721)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1131, 702))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.aquaBox = QtWidgets.QComboBox(parent=self.horizontalLayoutWidget)
        self.aquaBox.setFont(font)
        self.aquaBox.setObjectName("aquaBox")
        self.aquaBox.addItems(locs)
        self.gridLayout.addWidget(self.aquaBox, 0, 2, 1, 1)

        self.obstacleBox = QtWidgets.QComboBox(parent=self.horizontalLayoutWidget)
        self.obstacleBox.setFont(font)
        self.obstacleBox.setObjectName("obstacleBox")
        self.obstacleBox.addItems(names)
        self.gridLayout.addWidget(self.obstacleBox, 1, 2, 1, 1)

        self.button = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.button.setFont(font)
        self.button.setObjectName("button")
        self.button.setText("Применить")
        self.button.clicked.connect(self.button_clicked)
        self.gridLayout.addWidget(self.button, 2, 2, 1, 1)
        
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 3, 1, 1)

        self.label = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("Акватория:")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        
        self.label_2 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Метрика:")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        spacerItem3 = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        
        self.horizontalLayout.addLayout(self.verticalLayout)

        m = folium.Map(location=loc[0][0], zoom_start = loc[0][1])
        self.map = QtWebEngineWidgets.QWebEngineView(parent=self.horizontalLayoutWidget)
        self.map.setHtml(m.get_root().render())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.map.sizePolicy().hasHeightForWidth())
        self.map.setSizePolicy(sizePolicy)
        self.map.setMinimumSize(QtCore.QSize(700, 700))
        self.map.setMaximumSize(QtCore.QSize(700, 700))
        self.map.setObjectName("map")
        self.horizontalLayout.addWidget(self.map)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1056, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    # кнопка применить
    def button_clicked(self):
        self.del_map()
        
        m = folium.Map(location=loc[self.aquaBox.currentIndex()][0], zoom_start = loc[self.aquaBox.currentIndex()][1])
        f = self.aquaBox.currentIndex()
        c = self.obstacleBox.currentIndex()

        match self.obstacleBox.currentIndex():
            case 2:
                n = metric[self.aquaBox.currentIndex()][0]
                m = getData(m, [file[self.aquaBox.currentIndex()], self.aquaBox.currentIndex()], self.obstacleBox.currentIndex(), n)
            case _:
                n = metric[self.aquaBox.currentIndex()][1]
                m = getData(m, [file[self.aquaBox.currentIndex()], self.aquaBox.currentIndex()], self.obstacleBox.currentIndex(), n)
            
        self.make_map(m)    


    def make_map(self, m):
        self.map = QtWebEngineWidgets.QWebEngineView(parent=self.horizontalLayoutWidget)
        self.map.setHtml(m.get_root().render())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.map.sizePolicy().hasHeightForWidth())
        self.map.setSizePolicy(sizePolicy)
        self.map.setMinimumSize(QtCore.QSize(700, 700))
        self.map.setMaximumSize(QtCore.QSize(700, 700))
        self.map.setObjectName("map")
        self.horizontalLayout.addWidget(self.map)

    def del_map(self):
        self.map.setHtml('')
        self.map.page().profile().clearHttpCache()
        self.horizontalLayout.removeWidget(self.map)


# инициализация окна
app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
w = QtWebEngineWidgets.QWebEngineView()

window.show()
sys.exit(app.exec())