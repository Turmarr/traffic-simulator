from PyQt5 import QtWidgets, QtGui, QtCore
import math

class CarGraphicsItem(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, car):
        super(CarGraphicsItem, self).__init__()
        self.car = car
        self.color = self.set_color()
        self.setBrush(self.color)
        self.construct_car_outline()
        self.update_all()

    def set_color(self):
        red = QtGui.QColor.fromRgb(255, 0, 0)
        green = QtGui.QColor.fromRgb(0, 255, 0)
        blue = QtGui.QColor.fromRgb(0, 0, 255)
        yellow = QtGui.QColor.fromRgb(255, 255, 0)
        purple = QtGui.QColor(255, 0, 255)
        color = self.car.get_color()
        if color == 'red':
            return red
        if color == 'green':
            return green
        if color == 'blue':
            return blue
        if color == 'yellow':
            return yellow
        else:
            return purple

    def construct_car_outline(self):
        """
        This method sets the shape of the cari into an irregular hexagon to differentiate
        between front and back
        """
        car = QtGui.QPolygonF()

        car.append(QtCore.QPointF(0, 5))
        car.append(QtCore.QPointF(5, 0))
        car.append(QtCore.QPointF(15, 0))
        car.append(QtCore.QPointF(20, 5))
        car.append(QtCore.QPointF(20, 40))
        car.append(QtCore.QPointF(0, 40))
        car.append(QtCore.QPointF(0, 5))

        self.setPolygon(car)

        # rotation point should be near middle
        self.setTransformOriginPoint(10, 20)

    def update_all(self):
        self.update_position()
        self.update_rotation()

    def update_position(self):
        # updates the position of the car
        # have to check from which point it measures and if it is okay or do I need to relocate it to center
        pos = self.car.get_position()
        self.setPos(pos[0]-10, pos[1]-20)

    def update_rotation(self):
        orientation = self.car.get_orientation()
        deg = math.atan2(orientation[0], -orientation[1])*180/math.pi
        if deg < 0:
            deg = deg + 360
        #deg += 180
        self.setRotation(deg)