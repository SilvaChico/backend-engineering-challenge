from random import randint
import unittest
from datetime import datetime, timedelta
import argparse
import os
from unittest.mock import patch
from src.main import calculate_average
from src.main import convert_to_datetime
from src.main import format_events
from src.main import calculate_average_delivery_times
from src.main import main


class TestMainFunctions(unittest.TestCase):
    def test_calculate_average(self):
        self.assertEqual(calculate_average([10, 20, 30, 40, 0]), 25)

    def test_calculate_average_all_zeros(self):
        self.assertEqual(calculate_average([0, 0, 0]), 0)

    def test_convert_to_datetime(self):
        timestamp = "2020-01-01 00:00:00.000"
        self.assertEqual(convert_to_datetime(timestamp), datetime(2020, 1, 1, 0, 0))

    def test_convert_to_datetime_invalid_timestamp(self):
        timestamp = "2020-01-01 00:00:00"
        with self.assertRaises(ValueError):
            convert_to_datetime(timestamp)

    def test_convert_to_datetime_with_milliseconds(self):
        timestamp = "2020-01-01 00:00:00.123"
        self.assertEqual(
            convert_to_datetime(timestamp),
            datetime(2020, 1, 1, 0, 0, 0, 123000),
        )

    def test_format_events(self):
        events_strings = [
            {"timestamp": "2020-01-01 00:00:00.000", "duration": 10},
            {"timestamp": "2020-01-01 00:12:00.000", "duration": 20},
            {"timestamp": "2020-01-01 00:15:00.000", "duration": 30},
            {"timestamp": "2020-01-01 00:15:00.000", "duration": 40},
            {"timestamp": "2020-01-01 00:16:00.000", "duration": 0},
        ]
        expected = {
            datetime(2020, 1, 1, 0, 1): 10,
            datetime(2020, 1, 1, 0, 13): 20,
            datetime(2020, 1, 1, 0, 16): 70,
            datetime(2020, 1, 1, 0, 17): 0,
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

    def test_calculate_average_delivery_times_with_10k_events(self):
        base_timestamp = datetime.strptime(
            "2020-01-01 00:01:15.000", "%Y-%m-%d %H:%M:%S.%f"
        )
        events_strings = []

        for i in range(10000):
            timestamp = base_timestamp + timedelta(minutes=i)
            duration = 50
            event = {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "duration": duration,
            }
            events_strings.append(event)
        window = 10

        # except for the first minute, the average delivery time should be 50
        # because the duration is always 50
        any_index = 1321
        self.assertEqual(
            calculate_average_delivery_times(window, events_strings)[any_index][
                "average_delivery_time"
            ],
            50,
        )

    def test_main_with_empty_file(self):
        # create an empty temporary file
        with open("tests/temp_input.json", "w") as f:
            f.write("")

        with self.assertRaises(ValueError) as context:
            with patch(
                "argparse.ArgumentParser.parse_args",
                return_value=argparse.Namespace(
                    input_file="tests/temp_input.json", window_size=5
                ),
            ):
                main()

        self.assertEqual(str(context.exception), "The file is empty")

        # delete the temporary file
        os.remove("tests/temp_input.json")

    def test_main_with_empty_json(self):
        # create an empty temporary file
        with open("tests/temp_input.json", "w") as f:
            f.write("[]")

        with self.assertRaises(ValueError) as context:
            with patch(
                "argparse.ArgumentParser.parse_args",
                return_value=argparse.Namespace(
                    input_file="tests/temp_input.json", window_size=5
                ),
            ):
                main()

        self.assertEqual(str(context.exception), "The json is empty")

        # delete the temporary file
        os.remove("tests/temp_input.json")

    def test_main_with_window_0(self):
        # create an temporary file
        with open("tests/temp_input.json", "w") as f:
            f.write(
                '[{"timestamp": "2020-01-01 00:01:15.000", "duration": 10},'
                '{"timestamp": "2020-01-01 00:12:00.000", "duration": 20},'
                '{"timestamp": "2020-01-01 00:15:00.000", "duration": 30},'
                '{"timestamp": "2020-01-01 00:15:00.000", "duration": 40},'
                '{"timestamp": "2020-01-01 00:16:00.000", "duration": 0}]'
            )

        with self.assertRaises(ValueError) as context:
            with patch(
                "argparse.ArgumentParser.parse_args",
                return_value=argparse.Namespace(
                    input_file="tests/temp_input.json", window_size=0
                ),
            ):
                main()

        self.assertEqual(
            str(context.exception), "The window size must be greater than zero"
        )

        # delete the temporary file
        os.remove("tests/temp_input.json")
