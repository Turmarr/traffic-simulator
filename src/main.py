from PyQt5.QtWidgets import QApplication
from city_file_reader import *
from city import City
from gui import GUI


def main():
    city_info = load_city()

    global app
    app = QApplication(sys.argv)
    city = City(city_info)
    gui = GUI(city)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
