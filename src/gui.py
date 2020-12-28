from PyQt5 import QtWidgets, QtCore, QtGui

from car_graphics_item import CarGraphicsItem
#from building import Building

class GUI(QtWidgets.QMainWindow):

    def __init__(self, city):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)
        self.city = city
        self.buildings = []
        self.init_window(city.get_size())
        self.init_button()
        self.show()
        self.counter = 0

        self.on = False

        self.add_buildings(city.get_buildings())
        self.cars_with_graphicsitem = []
        self.add_car_graphicsitems()
        self.update_city()

        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.simulate_city())
        self.timer.timeout.connect(lambda: self.update_city())
        self.timer.start(self.city.time)  # Milliseconds

    def init_window(self, size):
        '''
        Sets up the window.
        '''
        self.setGeometry(300, 200, (size[0]*150)+150, (size[1]*150)+50)
        self.setWindowTitle('Traffic simulator')
        self.show()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, size[0]*150, size[1]*150)
        self.scene.setBackgroundBrush(QtGui.QColor.fromRgb(0,0,0))

        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)

    def init_button(self):
        self.toggle_btn = QtWidgets.QPushButton("Toggle simulation")
        self.toggle_btn.clicked.connect(lambda: self.toggle_simulation())
        self.horizontal.addWidget(self.toggle_btn)

    def add_buildings(self, buildings):
        for i in buildings:
            square = QtWidgets.QGraphicsRectItem(i[0]*150, i[1]*150, 150, 150)
            square.setBrush(QtGui.QColor.fromRgb(211, 211, 211))
            self.buildings.append(square)
            self.scene.addItem(square)

    def add_car_graphicsitems(self):
        for car in self.city.get_cars():
            if car in self.cars_with_graphicsitem:
                pass
            else:
                self.cars_with_graphicsitem.append(car)
                car = CarGraphicsItem(car)
                self.scene.addItem(car)

    def toggle_simulation(self):
        if not self.on:
            self.on = True
        else:
            self.on = False

    def simulate_city(self):
        if self.on:
            if self.counter == 0:
                self.city.create_car()
                self.add_car_graphicsitems()
            for car in self.city.get_cars():
                if car.get_finished():
                    self.cars_with_graphicsitem.remove(car)
                    self.city.remove_car(car)
                car.update_car(self.city.get_cars(), self.city.get_buildings())
            if self.counter == 0:
                self.counter -= self.city.interval
            self.counter += 1

    def update_city(self):
        for item in self.scene.items():
            if type(item) is CarGraphicsItem:
                if item.car.get_finished():
                    self.scene.removeItem(item)
                item.update_all()