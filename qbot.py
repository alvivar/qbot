""" Python Bot/library that queues tweets to post them later! """

from datetime import datetime
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


def get_schedule_column(day):
    """ Return the column day of the week assuming day index as days of the week
    (0-6). """
    if day == 0:
        return Schedule.monday
    elif day == 1:
        return Schedule.tuesday
    elif day == 2:
        return Schedule.wednesday
    elif day == 3:
        return Schedule.thursday
    elif day == 4:
        return Schedule.friday
    elif day == 5:
        return Schedule.saturday
    elif day == 6:
        return Schedule.sunday


def process_queue():

    # What day are we?
    today = datetime.today()
    day = today.weekday()
    hour = today.hour
    minute = today.minute

    print(f"Today {get_schedule_column(day)}")
    print(f"Hour {hour}")
    print(f"Minute {minute}")

    # Schedules for today below
    hours = DB.query(Time).join(Schedule).filter(
        get_schedule_column(day)).filter(
            and_(Time.hour <= hour, Time.minute <= minute))

    for hour in hours:

        print(f"Hour {hour.hour}.{hour.minute} used {hour.used}")

        # If the last published post older that the current hour?
        if hour.used is None or (hour.used < datetime.today()):

            # Get the first post unpublished post of the schedule in the hour
            post = DB.query(Post).filter(
                and_(Post.schedule_id == hour.schedule_id,
                     not Post.published)).first()

            # Tweet it!
            if post:

                print(f"Tweet: {post.text}")

                # Mark the post as published, and register the hour used time

                hour.used = datetime.now()
                post.published = True

                DB.add(hour)
                DB.add(post)
                DB.commit()


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
