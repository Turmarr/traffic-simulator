import sys
from corrupted_city_file_error import CorruptedCityFileError


def open_cityfile():
    filename = input("Please input the filename for the city.\n"
                     "The file extension is .city. "
                     "If no such file exists type q to exit.\n")
    while True:
        try:
            file = open(filename, "r")
        except OSError:
            if filename.strip() == "q":
                # if there is no file exits out of the program
                sys.exit()
            print("File not found, please try again.")
            print("If no such file exists type q to exit.")
            filename = input()
        else:
            return file


def read_size(file):
    while True:
        line = file.readline()
        line = line.replace(" ", "")
        line = line.strip()
        line = line.split(",")
        if len(line) == 2:
            try:
                x = int(line[0])
                y = int(line[1])
                if x > 0 and y > 0:
                    return (x, y)
                else:
                    file.close()
                    raise CorruptedCityFileError('Negative city size')
            except ValueError:
                file.close()
                raise CorruptedCityFileError('Invalid "size of city" block')


def read_interval(file):
    while True:
        line = file.readline()
        line = line.strip()
        try:
            interval = int(line)
            if interval > 0:
                return interval
            else:
                file.close()
                raise CorruptedCityFileError('Interval must be greater than 0')
        except ValueError:
            file.close()
            raise CorruptedCityFileError('Invalid "interval" block')


def read_simulation_speed(file):
    while True:
        line = file.readline()
        line = line.strip()
        try:
            time = int(line)
            if time > 0:
                return time
            else:
                file.close()
                raise CorruptedCityFileError('Time must be greater than 0')
        except ValueError:
            file.close()
            raise CorruptedCityFileError('Invalid "time" block')


def read_point(file, city, block):
    for line in file:
        if line[0] == "#":
            return line
        line = line.split(",")
        for i in range(len(line)):
            line[i] = line[i].strip()
        if line[0] != "" and len(line) == 2:
            try:
                x = int(line[0])
                y = int(line[1])
                if 0 <= x < city["size"][0] and 0 <= y < city["size"][1]:
                    if (x,y) not in city["building"] and (x,y) not in city[block]:
                        city[block].append((x, y))
                    else:
                        file.close()
                        raise CorruptedCityFileError("coordinates obstructed in block "+block)
                else:
                    file.close()
                    raise CorruptedCityFileError("coordinates outside of bounds in block "+block)
            except ValueError:
                file.close()
                raise CorruptedCityFileError('Invalid "'+block+'" block')
            #lisää tarkistus että ei talon sisällä


def read_cars(file, city):
    for line in file:
        if line[0] == '#':
            return line
        line = line.split(";")
        if len(line) == 3:
            for i in range(len(line)):
                line[i] = line[i].replace(" ", "")
                line[i] = line[i].strip().lower()
                line[i] = line[i].split(",")
            for i in range(2):
                for j in range(2):
                    try:
                        line[i][j] = int(line[i][j])
                    except ValueError:
                        file.close()
                        raise CorruptedCityFileError("Invalid car block")
                line[i] = (line[i][0], line[i][1])
            if 0 <= line[0][0] < city["size"][0] and 0 <= line[0][1] < city["size"][0]:
                if 0 <= line[1][0] < city["size"][0] and 0 <= line[1][1] < city["size"][0]:
                    if line[0] in city["startpoint"] and line[1] in city["startpoint"]:
                        city["car"]["start"].append(line[0])
                        city["car"]["stop"].append(line[1])
                        car_color = line[2][0]
                        city["car"]["color"].append(car_color)
                    else:
                        file.close()
                        raise CorruptedCityFileError("Coordinates not defined in block car")
                else:
                    file.close()
                    raise CorruptedCityFileError("Target coordinates out of bounds in block car")
            else:
                file.close()
                raise CorruptedCityFileError("Origin coordinates out of bounds in block car")


def load_city():
    file = open_cityfile()

    city = {"size": [], "building": [], "crosspoint": [], "startpoint": [], "interval": 0, "time": 0,
            "car": {"start": [], "stop": [], "color": []}}
    size_read = False
    building_read = False
    crosspoint_read = False
    startpoint_read = False
    interval_read = False
    car_read = False
    time_read = False
    try:
        line = file.readline()
        while line:
            lineflag = False
            line = list(line)

            if line[0] == '#':
                del(line[0])
                line = "".join(line)
                line = line.replace(" ", "")
                line = line.strip().lower()

                if line == "sizeofcity":
                    if not size_read:
                        city["size"] = read_size(file)
                        size_read = True
                    else:
                        raise CorruptedCityFileError("Two size of city blocks")

                if line == "building":
                    if size_read:
                        line = read_point(file, city, line)
                        building_read = True
                        lineflag = True
                    else:
                        file.close()
                        raise CorruptedCityFileError("Wrong order of chunks")

                if line == "startpoint":
                    if size_read and building_read:
                        line = read_point(file, city, line)
                        lineflag = True
                        startpoint_read = True
                    else:
                        file.close()
                        raise CorruptedCityFileError("Wrong order of chunks")

                if line == "crosspoint":
                    if size_read and building_read:
                        line = read_point(file, city, line)
                        lineflag = True
                        crosspoint_read = True
                    else:
                        file.close()
                        raise CorruptedCityFileError("Wrong order of chunks")

                if line == "car":
                    if size_read and startpoint_read:
                        line = read_cars(file, city)
                        lineflag = True
                        car_read = True
                    else:
                        file.close()
                        raise CorruptedCityFileError("Wrong order of chunks")

                if line == "interval":
                    city["interval"] = read_interval(file)
                    interval_read = True

                if line == "time":
                    city["time"] = read_simulation_speed(file)
                    time_read = True


            if not lineflag:
                line = file.readline()

        file.close()
        if not crosspoint_read or not building_read or not car_read or not time_read or not interval_read:
            raise CorruptedCityFileError("File is missing chunks")

        return city

    except OSError:
        file.close()
        raise CorruptedCityFileError("Reading the city's data failed")