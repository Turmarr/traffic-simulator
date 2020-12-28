import math


class Car:
    def __init__(self, start, stop, color, points):
        """
        points [x,y]
        position : format : [x,y]
        orientation : degrees
        path, list with target points
        """
        self.__finished = False
        self.__color = color
        self.__path = self.form_path(start, stop, points)
        self.__orientation = self.define_starting_orientation(self.__path)
        self.__position = self.define_starting_position(self.__orientation)
        self.__count_point = 0
        self.__target = [0, 0]
        self.update_target(self.__count_point)
        self.__outline = self.form_car_outline()

        self.__mass = 50
        self.__velocity = [0, 0]
        self.__max_force = 40
        self.__max_speed = 4

    def get_position(self):
        pos = []
        for i in range(2):
            pos.append(self.__position[i])
        return pos

    def get_finished(self):
        return self.__finished

    def get_path(self):
        return self.__path

    def get_orientation(self):
        direct = []
        for i in range(2):
            direct.append(self.__orientation[i])
        return direct

    def get_target(self):
        target = []
        for i in range(2):
            target.append(self.__target[i])
        return target

    def get_color(self):
        return self.__color

    def get_distance(self, pos1, pos2):
        distance = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
        return distance

    def update_target(self, count):
        count += 1
        if count < len(self.__path):
            self.__target = [self.__path[count][0] * 150 + 75, self.__path[count][1] * 150 + 75]
            self.__count_point = count
        else:
            self.__finished = True

    def get_tot_velocity(self):
        vel = math.sqrt(self.__velocity[0] ** 2 + self.__velocity[1] ** 2)
        return vel

    def seek_target(self, target):
        """
        targets the point on the map which is in target
        :param target: point on scene
        :return: none
        """
        # normalized_direction = self.normalize_vector(target)
        # steering_force = self.multiply_vector(normalized_direction, self.__max_force)
        drag = self.multiply_vector(self.get_orientation(), -(self.get_tot_velocity() / self.__max_speed))
        steering_force = [target[0] + drag[0], target[1] + drag[1]]
        acceleration = [steering_force[0] / self.__mass, steering_force[1] / self.__mass]

        velocity = [acceleration[0] + self.__velocity[0], acceleration[1] + self.__velocity[1]]
        total_velocity = math.sqrt(velocity[0] ** 2 + velocity[1] ** 2)
        if self.get_tot_velocity() > 0.9:
            self.__orientation = [velocity[0] / total_velocity, velocity[1] / total_velocity]
        if total_velocity > self.__max_speed:
            velocity = [(velocity[0] / total_velocity) * self.__max_speed,
                        (velocity[1] / total_velocity) * self.__max_speed]
        self.__velocity = velocity
        self.__position = [self.__position[0] + velocity[0], self.__position[1] + velocity[1]]

    def move_position(self, pos, vect):
        for i in range(2):
            pos[i] = pos[i] + vect[i]
        return pos

    def offset_target(self, target, amount):
        """
        Input: target = position, amount = by how much to offset it in direction of normal of direction of car
        returns: point
        if amount > 0 offset in direction pos 90 deg
        if amount < 0 offset in direction neg 90 deg
        """
        direct = self.get_orientation()
        offset_vector = [-direct[1], direct[0]]
        target = [target[0] + offset_vector[0] * amount, target[1] + offset_vector[1] * amount]
        return target

    def multiply_vector(self, vect, amount):
        """
        :param vect: the vector
        :param amount: len of vector amount > 0 pos amount < 0 -pos
        :return: vector of desired length in direction of vect
        """
        for i in range(2):
            vect[i] = vect[i] * amount
        return vect

    def form_car_outline(self):
        front_r = self.offset_target(self.move_position
                                     (self.get_position(), self.multiply_vector(self.get_orientation(), 20)), 10)
        front_l = self.offset_target(self.move_position
                                     (self.get_position(), self.multiply_vector(self.get_orientation(), 20)), -10)
        back_r = self.offset_target(self.move_position
                                    (self.get_position(), self.multiply_vector(self.get_orientation(), -20)), 10)
        back_l = self.offset_target(self.move_position
                                    (self.get_position(), self.multiply_vector(self.get_orientation(), -20)), -10)
        return (front_r, front_l, back_r, back_l)

    def form_building_outline(self, building):
        p1 = [building[0], building[1]]
        p2 = [building[0] + 150, building[1]]
        p3 = [building[0], building[1] + 150]
        p4 = [building[0] + 150, building[1] + 150]
        outline = [[p1, p2], [p2, p3], [p3, p4], [p4, p1]]
        return outline

    def construct_front_feelers(self, outline):
        feeler_l = self.move_position([outline[1][0], outline[1][1]], self.multiply_vector(self.get_orientation(), 30))
        feeler_r = self.move_position([outline[0][0], outline[0][1]], self.multiply_vector(self.get_orientation(), 30))
        feeler_c = self.move_position(self.get_position(), self.multiply_vector(self.get_orientation(), 50))
        return (feeler_r, feeler_c, feeler_l)

    def construct_side_feelers(self, outline):
        feeler_lf = self.offset_target(self.move_position([outline[1][0], outline[1][1]],
                                                          self.multiply_vector(self.get_orientation(), 10)), -10)
        feeler_lb = self.offset_target(self.move_position([outline[3][0], outline[3][1]],
                                                          self.multiply_vector(self.get_orientation(), -10)), -10)
        feeler_rf = self.offset_target(self.move_position([outline[0][0], outline[0][1]],
                                                          self.multiply_vector(self.get_orientation(), 10)), 10)
        feeler_rb = self.offset_target(self.move_position([outline[2][0], outline[2][1]],
                                                          self.multiply_vector(self.get_orientation(), -10)), 10)
        return [[feeler_lf, feeler_lb], [feeler_rf, feeler_rb]]

    def normalize_vector(self, vect):
        normalizing_factor = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        vect = [vect[0] / normalizing_factor, vect[1] / normalizing_factor]
        return vect

    def orientation(self, p1, p2, p3):
        orien = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p3[1] - p2[1]) * (p2[0] - p1[0])
        if orien > 0:
            return 1
        if orien < 0:
            return -1
        else:
            return 0

    def check_if_intersect(self, p1, p2, q1, q2):
        """
        basis for this and orientation() were from:
        https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
        """
        o1 = self.orientation(p1, p2, q1)
        o2 = self.orientation(p1, p2, q2)
        o3 = self.orientation(q1, q2, p1)
        o4 = self.orientation(q1, q2, p2)
        if o1 != o2 and o3 != o4:
            return True
        return False

    def braking(self, new_target):
        if self.get_tot_velocity() > 1:
            new_target = self.multiply_vector(new_target, -1)
        else:
            new_target = self.multiply_vector(new_target, 0)
            self.__velocity = [0, 0]
        return new_target

    def turning(self, new_target, amount):
        amount = amount * math.pi / 180
        new_target = [math.cos(amount) * new_target[0] - math.sin(amount) * new_target[1],
                      math.cos(amount) * new_target[1] + math.sin(amount) * new_target[0]]
        return new_target

    def define_behaviour(self, cars, buildings):
        braking = False
        target = self.get_target()
        own_outline = self.__outline
        f_feelers = self.construct_front_feelers(own_outline)
        s_feelers = self.construct_side_feelers(own_outline)

        target = self.offset_target(target, 35)
        steering_direction = [target[0] - self.__position[0], target[1] - self.__position[1]]
        normalized_direction = self.normalize_vector(steering_direction)
        new_target = self.multiply_vector(normalized_direction, self.__max_force)

        close_cars = []
        for car in cars:
            if self.get_distance(self.get_position(), car.get_position()) < 70 and car != self:
                close_cars.append(car)
        # (front_r, front_l, back_r, back_l)
        left_feeler = [own_outline[1], f_feelers[2]]
        right_feeler = [own_outline[0], f_feelers[0]]
        center_feeler = [self.get_position(), f_feelers[1]]
        feelers = [left_feeler, right_feeler, center_feeler]

        for car in close_cars:
            in_front = False
            on_left = False
            on_right = False
            outline = car.__outline
            front = ((outline[0][0], outline[0][1]), (outline[1][0], outline[1][1]))
            left = ((outline[0][0], outline[0][1]), (outline[2][0], outline[2][1]))
            right = ((outline[1][0], outline[1][1]), (outline[3][0], outline[3][1]))
            rear = ((outline[2][0], outline[2][1]), (outline[3][0], outline[3][1]))
            car_outline = [front, left, right, rear]
            for line in car_outline:
                for feeler in feelers:
                    if self.check_if_intersect(feeler[0], feeler[1], line[0], line[1]):
                        in_front = True
                        break
                if in_front:
                    break
            for line in car_outline:
                if self.check_if_intersect(s_feelers[0][0], s_feelers[0][1], line[0], line[1]):
                    on_left = True
            for line in car_outline:
                if self.check_if_intersect(s_feelers[1][0], s_feelers[1][1], line[0], line[1]):
                    on_right = True
            orientation = car.get_orientation()
            car_deg = math.atan2(orientation[0], orientation[1]) * 180 / math.pi
            own_deg = math.atan2(self.get_orientation()[0], self.get_orientation()[1]) * 180 / math.pi
            diff = car_deg - own_deg
            if diff < 0:
                diff += 360
            if in_front:
                if 0 <= diff < 45 or 315 < diff <= 360:
                    if not braking:
                        braking = True
                        new_target = self.braking(new_target)
                elif 45 <= diff < 135:
                    new_target = self.turning(new_target, 20)
                elif 135 <= diff < 225:
                    new_target = self.turning(new_target, 20)
                else:
                    if not braking:
                        braking = True
                        new_target = self.braking(new_target)

            if on_left:
                new_target = self.turning(new_target, 20)

            if on_right:
                if 135 <= diff < 225:
                    self.turning(new_target, -20)
                if 0 <= diff < 45 or 315 < diff <= 360:
                    if not braking:
                        braking = True
                        new_target = self.braking(new_target)

        '''for car in cars:
            if car != self:
                orientation = car.get_orientation()
                car_deg = math.atan2(orientation[0], orientation[1]) * 180 / math.pi
                own_deg = math.atan2(self.get_orientation()[0], self.get_orientation()[1]) * 180 / math.pi
                diff = car_deg - own_deg
                if diff < 0:
                    diff += 360
                projected_car = self.move_position(car.get_position(), self.multiply_vector(car.get_orientation(), 50))
                if self.check_if_intersect(self.get_position(), self.get_target(), car.get_position(), projected_car):
                    if 135 <= diff < 225:
                        if not braking:
                            new_target = self.braking(new_target)
'''
        bulding_in_front = False
        for build in buildings:
            lines = self.form_building_outline(build)
            for feeler in feelers:
                for line in lines:
                    if self.check_if_intersect(feeler[0], feeler[1], line[0], line[1]):
                        new_target = [0.94 * new_target[0] + 0.342 * new_target[1],
                                      0.94 * new_target[1] - 0.342 * new_target[0]]
                    break
            if bulding_in_front:
                break

        self.seek_target(new_target)

    def update_car(self, cars, buildings):
        pos = self.get_position()
        target = self.get_target()
        if self.get_distance(pos, self.__target) < 60:
            self.update_target(self.__count_point)
        self.define_behaviour(cars, buildings)

        self.__outline = self.form_car_outline()

    def form_path(self, start, stop, points):
        """ If there are multiple routes to the desired stop it shouldn't affect anything as long as the paths are of
        different length, and even then it should work """

        temp = []
        temp3 = []
        for point in points.keys():
            if stop in points[point]['startpoint']:
                temp3.append(point)
        temp.append(temp3)
        while True:
            flag = False
            i = len(temp) - 1
            temp2 = []
            # check if the end is reachable
            for point in temp[i]:
                if start in points[point]['startpoint']:
                    flag = True
                    break
            # add all connected points
            if flag:
                break
            for cross in temp[i]:
                for point in points.keys():
                    if cross in points[point]['crosspoint']:
                        if i != 0:
                            if point not in temp[i - 1]:
                                temp2.append(point)
                        else:
                            temp2.append(point)
            temp.append(temp2)
        # tidy all useless coordinates from the list
        path = [start]
        for j in temp[-1]:
            if start in points[j]['startpoint']:
                path.append(j)
                break
        del (temp[i])
        while len(temp) != 0:
            for i in temp[-1]:
                if path[-1] in points[i]['crosspoint']:
                    path.append(i)
                    del (temp[-1])
                    break
        path.append(stop)
        return path

    def define_starting_orientation(self, path):
        point_0 = path[0]
        point_1 = path[1]
        if point_0[0] == point_1[0]:
            if point_1[1] - point_0[1] > 0:
                return [0, 1]
            else:
                return [0, -1]
        else:
            if point_1[0] - point_0[0] > 0:
                return [1, 0]
            else:
                return [-1, 0]
        # return [0,-1]

    def define_starting_position(self, orientation):
        start = self.__path[0]
        start_x = start[0] * 150 + 75
        start_y = start[1] * 150 + 75
        if orientation[0] == -1:  # left
            start_y -= 40
        if orientation[1] == 1:  # down
            start_x -= 40
        if orientation[0] == 1:  # right
            start_y += 40
        if orientation[1] == -1:  # up
            start_x += 40

        return [start_x, start_y]
