import argparse
import json
import random
from datetime import datetime, timedelta

MAX_EVENT_COUNT = 10
# Facebook SDK standard events
# https://developers.facebook.com/docs/facebook-pixel/reference#standard-events
EVENT_TYPES = [
    "ADD_PAYMENT_INFO",
    "ADD_TO_CART",
    "ADD_TO_WISHLIST",
    "COMPLETE_REGISTRATION",
    "CONTACT",
    "CUSTOMIZE_PRODUCT",
    "FIND_LOCATION",
    "INITIATE_CHECKOUT",
    "LEAD",
    "PAGE_VIEW",
    "PURCHASE",
    "SCHEDULE",
    "SEARCH",
    "START_TRIAL",
    "SUBMIT_APPLICATION",
    "SUBSCRIBE",
    "VIEW_CONTENT",
]


def parse_appfile(location):
    apps = []
    with open(location, "r") as f:
        for line in f:
            apps.append(line.strip("\n"))
    return apps


def random_timestamp(min_year=2000, max_year=datetime.now().year):
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return random.random() * (end - start) + start


def random_past_events(app_name, event_count):
    data = {"name": app_name, "events": []}
    n = random.randint(1, event_count)
    for i in range(n):
        timestamp = random_timestamp().timestamp()
        event = {"type": random.choice(EVENT_TYPES), "timestamp": timestamp}
        data["events"].append(event)
    return data


def off_facebook(applications, event_strategy, event_count=MAX_EVENT_COUNT):
    data = {"off_facebook_activity": []}
    for app in applications:
        data["off_facebook_activity"].append(event_strategy(app, event_count))
    return json.dumps(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate random off-facebook activity"
    )
    parser.add_argument(
        "--applications",
        type=str,
        required=True,
        help="File containing a line-separated list of apps",
    )
    parser.add_argument(
        "--output",
        default="your_off-facebook_activity.json",
        help="Destination for generated json",
    )
    parser.add_argument(
        "--event-count",
        type=int,
        default=MAX_EVENT_COUNT,
        help="How many events are to be generated per app",
    )
    args = parser.parse_args()
    apps = parse_appfile(args.applications)
    with open(args.output, "w") as f:
        f.write(off_facebook(apps, random_past_events, args.event_count))
