import unittest
import datetime
from src.main import calculate_average
from src.main import convert_to_datetime
from src.main import format_events
from src.main import calculate_average_delivery_times


class TestMainFunctions(unittest.TestCase):
    def test_calculate_average(self):
        self.assertEqual(calculate_average([10, 20, 30, 40, 0]), 25)
        self.assertEqual(calculate_average([0, 0, 0]), 0)

    def test_convert_to_datetime(self):
        timestamp = "2020-01-01 00:00:00.000"
        self.assertEqual(
            convert_to_datetime(timestamp), datetime.datetime(2020, 1, 1, 0, 0)
        )

        # invalid timestamp
        timestamp = "2020-01-01 00:00:00"
        with self.assertRaises(ValueError):
            convert_to_datetime(timestamp)

    def test_format_events(self):
        events_strings = [
            {"timestamp": "2020-01-01 00:00:00.000", "duration": 10},
            {"timestamp": "2020-01-01 00:12:00.000", "duration": 20},
            {"timestamp": "2020-01-01 00:15:00.000", "duration": 30},
            {"timestamp": "2020-01-01 00:15:00.000", "duration": 40},
            {"timestamp": "2020-01-01 00:16:00.000", "duration": 0},
        ]
        expected = {
            datetime.datetime(2020, 1, 1, 0, 1): 10,
            datetime.datetime(2020, 1, 1, 0, 13): 20,
            datetime.datetime(2020, 1, 1, 0, 16): 70,
            datetime.datetime(2020, 1, 1, 0, 17): 0,
        }
        self.assertEqual(format_events(events_strings), expected)

    def test_calculate_average_delivery_times(self):
        events_strings = [
            {"timestamp": "2020-01-01 00:01:15.000", "duration": 10},
            {"timestamp": "2020-01-01 00:12:00.000", "duration": 20},
            {"timestamp": "2020-01-01 00:15:00.000", "duration": 30},
            {"timestamp": "2020-01-01 00:15:00.000", "duration": 40},
            {"timestamp": "2020-01-01 00:16:00.000", "duration": 0},
        ]
        window = 5
        expected = [
            {"date": "2020-01-01 00:01:00", "average_delivery_time": 0},
            {"date": "2020-01-01 00:02:00", "average_delivery_time": 10.0},
            {"date": "2020-01-01 00:03:00", "average_delivery_time": 10.0},
            {"date": "2020-01-01 00:04:00", "average_delivery_time": 10.0},
            {"date": "2020-01-01 00:05:00", "average_delivery_time": 10.0},
            {"date": "2020-01-01 00:06:00", "average_delivery_time": 10.0},
            {"date": "2020-01-01 00:07:00", "average_delivery_time": 0},
            {"date": "2020-01-01 00:08:00", "average_delivery_time": 0},
            {"date": "2020-01-01 00:09:00", "average_delivery_time": 0},
            {"date": "2020-01-01 00:10:00", "average_delivery_time": 0},
            {"date": "2020-01-01 00:11:00", "average_delivery_time": 0},
            {"date": "2020-01-01 00:12:00", "average_delivery_time": 0},
            {"date": "2020-01-01 00:13:00", "average_delivery_time": 20.0},
            {"date": "2020-01-01 00:14:00", "average_delivery_time": 20.0},
            {"date": "2020-01-01 00:15:00", "average_delivery_time": 20.0},
            {"date": "2020-01-01 00:16:00", "average_delivery_time": 45.0},
            {"date": "2020-01-01 00:17:00", "average_delivery_time": 45.0},
        ]

        self.assertEqual(
            calculate_average_delivery_times(window, events_strings), expected
        )


if __name__ == "__main__":
    unittest.main()
