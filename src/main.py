import datetime
from collections import deque
import argparse
import json
from pprint import pprint


def calculate_average(numbers):
    # remove zero from list
    non_zeros = [x for x in numbers if x != 0]
    if len(non_zeros) == 0:
        return 0
    return sum(non_zeros) / len(non_zeros)


# This assumes that we can have more than one event in a minute
def get_durantion_last_minute(events, current_time):
    durations_last_minute = 0
    for event in events:
        if (
            current_time - datetime.timedelta(minutes=1)
            <= event["timestamp"]
            < current_time
        ):
            durations_last_minute += event["duration"]

    return durations_last_minute


def get_events(events_strings):
    """Convert the timestamps to datetime objects"""
    return [
        {
            "timestamp": datetime.datetime.strptime(
                event_string["timestamp"], "%Y-%m-%d %H:%M:%S.%f"
            ),
            "duration": event_string["duration"],
        }
        for event_string in events_strings
    ]


def calculate_average_delivery_times(window, events_strings):
    events = get_events(events_strings)

    start_time = events[0]["timestamp"].replace(second=0, microsecond=0)
    end_time = events[-1]["timestamp"] + datetime.timedelta(minutes=1)

    event_queue = deque([0] * (window))

    average_delivery_times = []
    current_time = start_time
    while current_time <= end_time:
        durations_last_minute = get_durantion_last_minute(events, current_time)
        event_queue.append(durations_last_minute)
        event_queue.popleft()

        average_delivery_times.append(
            f"{{\"date\": \"{current_time.strftime('%Y-%m-%d %H:%M:%S')}\", \"average_delivery_time\": {calculate_average(event_queue)}}}"
        )

        current_time += datetime.timedelta(minutes=1)
    return average_delivery_times


def main():
    # Create the parser
    parser = argparse.ArgumentParser()

    # Add the arguments
    parser.add_argument(
        "--input_file", type=str, required=True, help="The path to the input JSON file"
    )
    parser.add_argument(
        "--window_size", type=int, required=True, help="The window size"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Get the window size and input file
    window_size = args.window_size
    input_file = args.input_file

    # Load the events from the input file
    with open(input_file, "r") as f:
        events_strings = json.load(f)

    average_delivery_times = calculate_average_delivery_times(
        window_size, events_strings
    )
    for time in average_delivery_times:
        print(time)


if __name__ == "__main__":
    main()
