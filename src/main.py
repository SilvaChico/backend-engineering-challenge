import datetime
from collections import deque
import argparse
import json


def calculate_average(numbers):
    non_zeros = [x for x in numbers if x != 0]
    if len(non_zeros) == 0:
        return 0
    return sum(non_zeros) / len(non_zeros)


def convert_to_datetime(timestamp):
    return datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")


def format_events(events_strings):
    # convert the timestamps to datetime objects and the durations to integers and puts the into a dict
    formated_events = {}
    for event in events_strings:
        event_minute = convert_to_datetime(event["timestamp"]).replace(
            second=0, microsecond=0
        ) + datetime.timedelta(minutes=1)
        formated_events[event_minute] = formated_events.get(event_minute, 0) + int(
            event["duration"]
        )
    return formated_events


def calculate_average_delivery_times(window, events_strings):
    start_time = convert_to_datetime(events_strings[0]["timestamp"]).replace(
        second=0, microsecond=0
    )
    end_time = convert_to_datetime(
        events_strings[-1]["timestamp"]
    ) + datetime.timedelta(minutes=1)

    # creates a queue with the size of the window
    event_queue = deque([0] * (window))

    events = format_events(events_strings)
    average_delivery_times = []
    current_time = start_time
    while current_time <= end_time:
        # gets the duration of the events in the last minute
        durations_last_minute = events.get(current_time, 0)
        # adds the duration to the queue
        event_queue.appendleft(durations_last_minute)
        event_queue.pop()

        average_delivery_times.append(
            {
                "date": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "average_delivery_time": calculate_average(event_queue),
            }
        )

        current_time += datetime.timedelta(minutes=1)

    return average_delivery_times


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_file", type=str, required=True, help="The path to the input JSON file"
    )
    parser.add_argument(
        "--window_size", type=int, required=True, help="The window size"
    )

    args = parser.parse_args()

    window_size = args.window_size
    input_file = args.input_file

    with open(input_file, "r") as f:
        events_strings = json.load(f)

    average_delivery_times = calculate_average_delivery_times(
        window_size, events_strings
    )

    with open("output.json", "w") as f:
        json.dump(average_delivery_times, f)

    print("The average delivery times can be found in output.json")


if __name__ == "__main__":
    main()
