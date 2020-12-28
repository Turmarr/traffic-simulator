from car import Car
from random import randint

class City():
    def __init__(self, city_info):
        self.__building = city_info['building']
        self.__size = city_info['size']
        self.__startpoint = city_info['startpoint']
        # links the crosspoints to make it easyer to make the paths for the cars
        self.__crosspoint = self.link_crosspoints(city_info['crosspoint'], self.__startpoint, self.__building,
                                                  self.__size)
        # adds the cars with paths. One car is an object
        self.__carlist = city_info['car']
        self.__cars = []
        self.interval = city_info['interval']
        self.time = city_info['time']

    def get_carlist(self):
        return self.__carlist

    def get_buildings(self):
        return self.__building

    def get_size(self):
        return self.__size

    def get_startpoint(self):
        return self.__startpoint

    def get_crosspoint(self):
        return self.__crosspoint

    def get_cars(self):
        return self.__cars

    def link_crosspoints(self, crosspoints, startpoints, building, size):
        points = {}
        for i in crosspoints:
            point = {'startpoint': [], 'crosspoint': []}

            # +x direction
            j = 1
            flag = False
            while True:
                if i[0] + j == size[0] or flag:
                    break
                if (i[0] + j, i[1]) in building:
                    break
                for x in crosspoints:
                    if (i[0] + j, i[1]) == x:
                        point['crosspoint'].append(x)
                        flag = True
                        break
                if flag:
                    continue
                for x in startpoints:
                    if (i[0] + j, i[1]) == x:
                        point['startpoint'].append(x)
                        flag = True
                        break
                if flag:
                    continue
                j += 1
            # +y direction
            j = 1
            flag = False
            while True:
                if i[1] + j == size[1] or flag:
                    break
                if (i[0], i[1] + j) in building:
                    break
                for x in crosspoints:
                    if (i[0], i[1] + j) == x:
                        point['crosspoint'].append(x)
                        flag = True
                        break
                if flag:
                    continue
                for x in startpoints:
                    if (i[0], i[1] + j) == x:
                        point['startpoint'].append(x)
                        flag = True
                        break
                if flag:
                    continue
                j += 1
            # -x direction
            j = 1
            flag = False
            while True:
                if i[0] - j < 0 or flag:
                    break
                if (i[0] - j, i[1]) in building:
                    break
                for x in crosspoints:
                    if (i[0] - j, i[1]) == x:
                        point['crosspoint'].append(x)
                        flag = True
                        break
                if flag:
                    continue
                for x in startpoints:
                    if (i[0] - j, i[1]) == x:
                        point['startpoint'].append(x)
                        flag = True
                        break
                if flag:
                    continue
                j += 1
            # -y direction
            j = 1
            flag = False
            while True:
                if i[1] - j < 0 or flag:
                    break
                if (i[0], i[1] - j) in building:
                    break
                for x in crosspoints:
                    if (i[0], i[1] - j) == x:
                        point['crosspoint'].append(x)
                        flag = True
                        break
                if flag:
                    continue
                for x in startpoints:
                    if (i[0], i[1] - j) == x:
                        point['startpoint'].append(x)
                        flag = True
                        break
                if flag:
                    continue
                j += 1
            points[i] = point
        return points

    def create_car(self):
        '''
        generates a random car from the available car patterns
        :param cars: cars designated in file
        :return: returns a car object
        '''
        j = len(self.__carlist['start'])
        i = randint(0, j-1)
        car = Car(self.__carlist['start'][i], self.__carlist['stop'][i], self.__carlist['color'][i], self.__crosspoint)
        obstructed = False
        for other in self.get_cars():
            if other.get_path()[0] == car.get_path()[0] and car.get_distance(other.get_position(),
                                                                             car.get_position()) < 100:
                obstructed = True
        if not obstructed:
            self.__cars.append(car)

    def remove_car(self, car):
        self.__cars.remove(car)