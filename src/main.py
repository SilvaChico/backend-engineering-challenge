import datetime
from collections import deque
import argparse
import json


def calculate_average(numbers):
    """Calculates the average of a list of numbers, ignoring the zeros"""
    non_zeros = [x for x in numbers if x != 0]
    if len(non_zeros) == 0:
        return 0
    return sum(non_zeros) / len(non_zeros)


def convert_to_datetime(timestamp):
    """Converts a timestamp string to a datetime object"""
    return datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")


def format_events(events_strings):
    """Formats the events into a dict with the minute as the key and the total duration as the value"""
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
    """Calculates the average delivery times for each minute in the window"""
    start_time = convert_to_datetime(events_strings[0]["timestamp"]).replace(
        second=0, microsecond=0
    )
    end_time = convert_to_datetime(
        events_strings[-1]["timestamp"]
    ) + datetime.timedelta(minutes=1)

    # creates a queue with the size of the window
    event_queue = deque([0] * (window))

    events = format_events(events_strings)
    average_delivery_times_per_date = []
    current_time = start_time
    while current_time <= end_time:
        # gets the duration of the events in the last minute
        last_minute_total_durations = events.get(current_time, 0)
        # adds the duration to the queue
        event_queue.appendleft(last_minute_total_durations)
        event_queue.pop()

        average_delivery_times_per_date.append(
            {
                "date": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "average_delivery_time": calculate_average(event_queue),
            }
        )

        current_time += datetime.timedelta(minutes=1)

    return average_delivery_times_per_date


def main():
    """Main function"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_file", type=str, required=True, help="The path to the input JSON file"
    )
    parser.add_argument(
        "--window_size", type=int, required=True, help="The window size"
    )

    args = parser.parse_args()

    window_size = args.window_size
    if window_size <= 0:
        raise ValueError("The window size must be greater than zero")

    input_file = args.input_file

    with open(input_file, "r") as f:
        if f.read().strip() == "":
            raise ValueError("The file is empty")
        f.seek(0)  # reset file pointer to the beginning
        events_strings = json.load(f)

    if len(events_strings) == 0:
        raise ValueError("The json is empty")

    average_delivery_times = calculate_average_delivery_times(
        window_size, events_strings
    )

    with open("output.json", "w") as f:
        json.dump(average_delivery_times, f)

    print("The average delivery times can be found in output.json")


if __name__ == "__main__":
    main()
