""" Python Bot/library that queues tweets to post them later! """

import datetime
import json
import os
import sys
import time

# Database SQLAlchemy + SQLite
from qdb import Post, Schedule, Time, and_, init_database, sessionmaker

ENGINE = init_database()
SESSION = sessionmaker(bind=ENGINE)
DB = SESSION()


def update_schedule(name, days, hours):
    """ Create or update and return a schedule, assuming days as a list of
    numbers enumerating the days of the week (0-6) and hours a list of tuples of
    hours and minutes. """

    # Get
    schedule = DB.query(Schedule).filter(Schedule.name == name).first()

    # Or create
    if schedule is None:
        schedule = Schedule()
        schedule.name = name
        DB.add(schedule)
        DB.flush()

    # Days of the week
    schedule.monday = True if 0 in days else False
    schedule.tuesday = True if 1 in days else False
    schedule.wednesday = True if 2 in days else False
    schedule.thursday = True if 3 in days else False
    schedule.friday = True if 4 in days else False
    schedule.saturday = True if 5 in days else False
    schedule.sunday = True if 6 in days else False

    # New hours
    DB.query(Time).filter(Time.schedule_id == schedule.id).delete()
    for h_m in hours:
        hour = Time()
        hour.hour = h_m[0]
        hour.minute = h_m[1]
        hour.schedule_id = schedule.id
        DB.add(hour)

    # Save
    DB.commit()

    return schedule


def create_post(schedule_name, text, image_url):
    """ Create a post, return it. If the schedule doesn't exist, create it. """

    # Get
    schedule = DB.query(Schedule).filter(
        Schedule.name == schedule_name).first()

    # Or create
    if schedule is None:
        schedule = Schedule()
        schedule.name = schedule_name

        DB.add(schedule)
        DB.flush()

    # New post
    post = Post()
    post.text = text
    post.image_url = image_url
    post.schedule_id = schedule.id

    DB.add(post)
    DB.commit()

    return post


def get_schedule_column_day(dayindex):
    """ Return the column day of the week assuming day index as days of the week
    (0-6). """
    if dayindex == 0:
        return Schedule.monday
    elif dayindex == 1:
        return Schedule.tuesday
    elif dayindex == 2:
        return Schedule.wednesday
    elif dayindex == 3:
        return Schedule.thursday
    elif dayindex == 4:
        return Schedule.friday
    elif dayindex == 5:
        return Schedule.saturday
    elif dayindex == 6:
        return Schedule.sunday


def process_queue():

    # What day are we?
    day = datetime.datetime.today().weekday()
    hour = datetime.datetime.today().hour
    minute = datetime.datetime.today().minute

    print(f"Today {get_schedule_column_day(day)}")
    print(f"Hour {hour}")
    print(f"Minute {hour}")

    # Schedules for today below
    hours = DB.query(Time).join(Schedule).filter(
        get_schedule_column_day(day)).filter(
            and_(Time.hour <= 10, Time.minute <= minute))

    for h in hours:

        print(h.hour)

        # If the last published post older that the current hour?

        # Get the first post unpublished post of the schedule in the hour

        # Tweet it!

        # Mark the post as published

        # Register the hour used time


if __name__ == "__main__":

    DELTA = time.time()
    print("QBot\n")

    # Frozen / not frozen, cxfreeze compatibility
    DIR = os.path.normpath(
        os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else __file__))
    os.chdir(DIR)

    # Files
    TOKENS_FILE = "tokens.json"

    # Twitter tokens are mandatory
    try:
        TOKENS = json.load(open(TOKENS_FILE, 'r'))
    except (IOError, ValueError):
        TOKENS = {
            'consumer_key': "",
            'consumer_secret': "",
            'oauth_token': "",
            'oauth_secret': ""
        }
        with open(TOKENS_FILE, "w") as f:
            json.dump(TOKENS, f)
