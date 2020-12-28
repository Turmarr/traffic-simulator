import unittest
from unittest.mock import patch

from city_file_reader import *
from corrupted_city_file_error import CorruptedCityFileError

class File_reader_tests(unittest.TestCase):

    def test_correct_file(self,):
        with patch('builtins.input', return_value= "test_scripts/correct_file.city"):
            result = load_city()
        supposed = {'size': (4, 4), 'building': [(1, 3), (3, 0), (1, 1), (2, 2)],
                    'crosspoint': [(0, 0), (0, 2), (2, 0), (2, 1), (3, 1), (3, 3)],
                    'startpoint': [(1, 2), (2, 3), (0, 3)],
                    'time': 50, 'interval': 40,
                    'car': {'start': [(1, 2), (2, 3), (0, 3)], 'stop': [(2, 3), (1, 2), (2, 3)],
                            'color': ['red', 'green', 'yellow']}}
        self.assertEqual(result, supposed)

    def test_car_fourth_before_cross(self):
        with patch('builtins.input', return_value="test_scripts/car_before_cross.city"):
            result = load_city()
        supposed = {'size': (4, 4), 'building': [(1, 3), (3, 0), (1, 1), (2, 2)],
                    'crosspoint': [(0, 0), (0, 2), (2, 0), (2, 1), (3, 1), (3, 3)],
                    'startpoint': [(1, 2), (2, 3), (0, 3)],
                    'time': 50, 'interval': 40,
                    'car': {'start': [(1, 2), (2, 3), (0, 3)], 'stop': [(2, 3), (1, 2), (2, 3)],
                            'color': ['red', 'green', 'yellow']}}
        self.assertEqual(result, supposed)

    def test_chunked_file(self):
        with patch('builtins.input', return_value= "test_scripts/chunked_file.city"):
            result = load_city()
        supposed = {'size': (4, 4), 'building': [(1, 3), (3, 0), (1, 1), (2, 2)],
                    'crosspoint': [(0, 0), (0, 2), (2, 0), (2, 1), (3, 1), (3, 3)],
                    'startpoint': [(1, 2), (2, 3), (0, 3)],
                    'time': 50, 'interval': 40,
                    'car': {'start': [(1, 2), (2, 3), (0, 3)], 'stop': [(2, 3), (1, 2), (2, 3)],
                            'color': ['red', 'green', 'yellow']}}
        self.assertEqual(result, supposed)

    def test_building_first(self):
        with patch('builtins.input', return_value= "test_scripts/building_first.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Wrong order of chunks', lambda: load_city())

    def test_car_first(self):
        with patch('builtins.input', return_value= "test_scripts/car_first.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Wrong order of chunks', lambda: load_city())

    def test_startpoint_first(self):
        with patch('builtins.input', return_value= "test_scripts/startpoint_first.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Wrong order of chunks', lambda: load_city())

    def test_crosspoint_first(self):
        with patch('builtins.input', return_value= "test_scripts/crosspoint_first.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Wrong order of chunks', lambda: load_city())

    def test_crosspoint_second(self):
        with patch('builtins.input', return_value= "test_scripts/crosspoint_second.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Wrong order of chunks', lambda: load_city())

    def test_startpoint_second(self):
        with patch('builtins.input', return_value= "test_scripts/startpoint_second.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Wrong order of chunks', lambda: load_city())

    def test_car_second(self):
        with patch('builtins.input', return_value= "test_scripts/car_second.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Wrong order of chunks', lambda: load_city())

    def test_car_third(self):
        with patch('builtins.input', return_value= "test_scripts/car_third.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Wrong order of chunks', lambda: load_city())

    def test_car_fourth_before_start(self):
        with patch('builtins.input', return_value= "test_scripts/car_before_start.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Wrong order of chunks', lambda: load_city())

    def test_no_car(self):
        with patch('builtins.input', return_value= "test_scripts/no_car.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'File is missing chunks', lambda: load_city())

    def test_no_time(self):
        with patch('builtins.input', return_value= "test_scripts/no_time.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'File is missing chunks', lambda: load_city())

    def test_no_interval(self):
        with patch('builtins.input', return_value= "test_scripts/no_interval.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'File is missing chunks', lambda: load_city())

    def test_no_cross(self):
        with patch('builtins.input', return_value= "test_scripts/no_cross.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'File is missing chunks', lambda: load_city())

    def test_no_start(self):
        # basically the same as having the car before start block
        with patch('builtins.input', return_value= "test_scripts/no_start.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Wrong order of chunks', lambda: load_city())

    def test_invalid_car_startpoints(self):
        with patch('builtins.input', return_value= "test_scripts/invalid_start_for_car.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Coordinates not defined in block car', lambda: load_city())

    def test_target_coordinates_out_of_bounds(self):
        with patch('builtins.input', return_value= "test_scripts/target_coordinates_oob.city"):
            self.assertRaisesRegex(CorruptedCityFileError,
                                   'Target coordinates out of bounds in block car', lambda: load_city())

    def test_target_coordinates_out_of_bounds2(self):
        with patch('builtins.input', return_value= "test_scripts/target_coordinates_oob2.city"):
            self.assertRaisesRegex(CorruptedCityFileError,
                                   'Target coordinates out of bounds in block car', lambda: load_city())

    def test_invalid_car(self):
        with patch('builtins.input', return_value= "test_scripts/invalid_car.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Invalid car block', lambda: load_city())

    def test_origin_coordinates_out_of_bounds(self):
        with patch('builtins.input', return_value= "test_scripts/origin_coordinates_oob.city"):
            self.assertRaisesRegex(CorruptedCityFileError,
                                   'Origin coordinates out of bounds in block car', lambda: load_city())

    def test_origin_coordinates_out_of_bounds2(self):
        with patch('builtins.input', return_value= "test_scripts/origin_coordinates_oob2.city"):
            self.assertRaisesRegex(CorruptedCityFileError,
                                   'Origin coordinates out of bounds in block car', lambda: load_city())

    def test_negative_city_size(self):
        with patch('builtins.input', return_value= "test_scripts/negative_size.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Negative city size', lambda: load_city())

    def test_invalid_size(self):
        with patch('builtins.input', return_value= "test_scripts/invalid_size.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Invalid "size of city" block', lambda: load_city())

    def test_point_in_building(self):
        with patch('builtins.input', return_value= "test_scripts/point_in_building.city"):
            self.assertRaisesRegex(CorruptedCityFileError,
                                   'coordinates obstructed in block startpoint', lambda: load_city())

    def test_invalid_point(self):
        with patch('builtins.input', return_value= "test_scripts/invalid_point.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Invalid "building" block', lambda: load_city())

    def test_point_out_of_bounds(self):
        with patch('builtins.input', return_value= "test_scripts/point_oob.city"):
            self.assertRaisesRegex(CorruptedCityFileError,
                                   'coordinates outside of bounds in block building', lambda: load_city())

    def test_point_out_of_bounds2(self):
        with patch('builtins.input', return_value= "test_scripts/point_oob2.city"):
            self.assertRaisesRegex(CorruptedCityFileError,
                                   'coordinates outside of bounds in block building', lambda: load_city())

    def test_negative_time(self):
        with patch('builtins.input', return_value= "test_scripts/negative_time.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Time must be greater than 0', lambda: load_city())

    def test_invalid_time(self):
        with patch('builtins.input', return_value= "test_scripts/invalid_time.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Invalid "time" block', lambda: load_city())

    def test_negative_interval(self):
        with patch('builtins.input', return_value= "test_scripts/negative_interval.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Interval must be greater than 0', lambda: load_city())

    def test_invalid_interval(self):
        with patch('builtins.input', return_value= "test_scripts/invalid_interval.city"):
            self.assertRaisesRegex(CorruptedCityFileError, 'Invalid "interval" block', lambda: load_city())