""" Python Bot/library that queues tweets to post them later! """

import argparse
import json
import os
import sys
import threading
import time
from datetime import datetime

import tweepy
from sqlalchemy import and_

from qdb import Post, Schedule, Time, Watch, init_database, sessionmaker

# Constants
TOKENS_FILE = "tokens.json"

# SQLAlchemy + SQLite
ENGINE = init_database()
SESSION = sessionmaker(bind=ENGINE)
DB = SESSION()


def get_int_day(strday):
    """
        Return the Schedule.day of the week assuming 'day' as an index from
        (0-6).
    """

    strday = strday.lower()
    if strday == "monday":
        return 0
    elif strday == "tuesday":
        return 1
    elif strday == "wednesday":
        return 2
    elif strday == "thursday":
        return 3
    elif strday == "friday":
        return 4
    elif strday == "saturday":
        return 5
    elif strday == "sunday":
        return 6
    else:
        return -1


def get_schedule_column(day):
    """
        Return the Schedule.day of the week assuming 'day' as an index from
        (0-6).
    """

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


def update_schedule(name, days, hours):
    """
        Create or update and return a schedule, assuming days as a list of
        numbers enumerating the days of the week (0-6) and hours a list of
        tuples of hours and minutes [(h m), ...].
    """

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


def queue_post(schedule_name, text, image_url=None):
    """
        Create a post, return it. If the schedule doesn't exist, create it.
    """

    # Get
    schedule = DB.query(Schedule).filter(
        Schedule.name == schedule_name).first()

    # Or create
    if schedule is None:
        schedule = Schedule()
        schedule.name = schedule_name

        DB.add(schedule)
        DB.flush()

    # If repeated, rollback
    post = DB.query(Post).filter(
        and_(Post.schedule_id == schedule.id, Post.text == text)).first()

    if post:
        DB.rollback()
        return post

    # New post
    post = Post()

    post.text = text
    post.image_url = image_url
    post.schedule_id = schedule.id

    DB.add(post)
    DB.commit()

    return post


def watch_json(filename):
    """
        Create a json file that is going to be used as config / communication
        for the bot every time before processing a queue.
    """

    jsonmessage = {
        "options": {
            "refresh_schedule": True
        },
        "schedule": {
            "name":
            "example",
            "days": [
                "monday", "tuesday", "wednesday", "thursday", "friday",
                "saturday", "sunday"
            ],
            "hours":
            ["10:30", "12:30", "14:30", "16:30", "18:30", "20:30", "22:30"]
        },
        "twitter_tokens": {
            "consumer_key": "find",
            "consumer_secret": "them",
            "oauth_token": "on",
            "oauth_secret": "apps.twitter.com"
        },
        "messages": [{
            "text": "only text message #example"
        }, {
            "text": "message with an image #example",
            "image": "c:/somewhere/image.gif"
        }]
    }

    # File creation

    if os.path.isdir(filename):
        path = filename
        name = "qbot"
    else:
        path = os.path.dirname(filename)
        name = os.path.basename(filename)

    if not os.path.exists(path):
        os.makedirs(path)

    name, _ = os.path.splitext(name)
    filename = os.path.normpath(os.path.join(path, name + ".json"))

    # Add it to the watch list

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(jsonmessage, f, indent=True)
    print(f"Added to the watch list: '{filename}'")

    watch = DB.query(Watch).filter(Watch.path == filename).first()
    if watch is None:
        watch = Watch()
        watch.path = filename
        DB.add(watch)
        DB.commit()


def update_from_file(jsonfile):
    """
        The  json file contains all needed information for a working queue. The
        schedule will be created/updated, the messages will be queued, the
        tokens will be updated and the file will be modified to reflect changes.

        Check out the json inside 'watch_json(' function as reference.
    """

    try:
        message = json.load(open(jsonfile, 'r'))
    except (IOError, ValueError):
        print(f"This file doesn't exists or isn't a valid json: '{jsonfile}'")
        return

    # Schedule

    schedule = message['schedule']['name']
    days = [get_int_day(i) for i in message['schedule']['days']]
    hours = [tuple(x.split(":")) for x in message['schedule']['hours']]

    print(f"\nUpdating '{schedule}' from\n'{jsonfile}'")

    if message['options']["refresh_schedule"]:
        update_schedule(schedule, days, hours)
        message['options']["refresh_schedule"] = False
        print(f"New schedule updated")

    # Posts
    for i, post in enumerate(message['messages']):
        text = post['text']
        image = post['image'] if "image" in post else None
        queue_post(schedule, text, image)
        print(f"\n#{i+1} New post queued:\n{text} {image if image else ''}")

    # Response is in the same file

    message['queued'] = message.get('queued', [])
    message['queued'] += message['messages']
    message['messages'] = []

    with open(jsonfile, "w") as f:
        json.dump(message, f, indent=True)

    # Tokens

    try:
        tokens = json.load(open(TOKENS_FILE, 'r'))
    except (IOError, ValueError):
        tokens = {}

    tokens[schedule] = {
        'consumer_key': message['twitter_tokens']['consumer_key'],
        'consumer_secret': message['twitter_tokens']['consumer_secret'],
        'oauth_token': message['twitter_tokens']['oauth_token'],
        'oauth_secret': message['twitter_tokens']['oauth_secret']
    }

    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=True)


def process_queue(tokens):
    """
        First update all schedules and data from the watch list files, then
        tweet queued post based on the schedules. One at a time.
    """

    # Update data from the watch list

    print(f"Updating data from files in the watch list...")

    watch = DB.query(Watch).all()
    for w in watch:
        update_from_file(w.path)

    # What day are we?
    today = datetime.today()

    strday = str(get_schedule_column(today.weekday())).replace("Schedule.", "")
    print(f"\nQueue processing started "
          f"({strday.title()} {today.date()} {today.hour}:{today.minute:02})")

    # Get all the schedules for today
    todaysched = DB.query(Schedule).filter(
        get_schedule_column(today.weekday())).all()

    if not todaysched:
        print("No schedules today")

    # Look for an hour that fits
    for tsc in todaysched:

        hour = DB.query(Time).filter(
            and_(Time.schedule_id == tsc.id, Time.used < today.date(),
                 Time.hour + Time.minute / 100 <=
                 today.hour + today.minute / 100)).first()

        print(f"\nSchedule '{tsc.name}'")

        if hour:

            print(f"At {hour.hour}:{hour.minute:02}")

            # Get the first unpublished post of the schedule in the hour
            post = DB.query(Post).filter(
                and_(Post.schedule_id == hour.schedule_id,
                     Post.published == 0)).first()

            if post:

                # Announce

                print(
                    f"Trying to tweet:\n{post.text} {post.image_url if post.image_url else ''}"
                )

                # Twitter auth and tokens validation

                auth = tweepy.OAuthHandler(tokens[tsc.name]['consumer_key'],
                                           tokens[tsc.name]['consumer_secret'])
                auth.set_access_token(tokens[tsc.name]['oauth_token'],
                                      tokens[tsc.name]['oauth_secret'])

                if not tokens[tsc.name]['consumer_key']:
                    print(
                        f"The schedule '{tsc.name}' doesn't have the Twitter tokens, add them to the tokens file!"
                    )
                    continue

                # Tweet

                else:

                    api = tweepy.API(
                        auth,
                        wait_on_rate_limit=True,
                        wait_on_rate_limit_notify=True)

                    try:
                        if post.image_url:
                            api.update_with_media(post.image_url, post.text)
                        else:
                            api.update_status(post.text)
                        print(f"Done!")

                        # Mark the post as published, and register the hour used time

                        post.published = True
                        DB.add(post)

                        hour.used = datetime.now()
                        DB.add(hour)

                        DB.commit()

                    except tweepy.error.TweepError as err:
                        img = post.image_url if post.image_url is not None else ""
                        print(f"Skipped, error: {err}")

                        # TODO Mark the post as error instead of published
                        post.published = True
                        DB.add(post)
                        DB.commit()

            else:
                print("The queue is empty!")

        else:
            print(f"No pending hours!")


def prune_watch_list():
    """
        Delete orphan files from the watch list.
    """

    watch = DB.query(Watch).all()
    for w in watch:
        if not os.path.exists(w.path):
            DB.delete(w)
            print(f"Pruned: '{w.path}'")
    DB.commit()
    print(f"Watch list clean!")


if __name__ == "__main__":

    DELTA = time.time()

    print("""
     ["]
    /[_]\\
     ] [""")

    # Command line args

    PARSER = argparse.ArgumentParser(
        description=
        'Bot that tweets on schedules, using json files as configuration')
    PARSER.add_argument(
        "-w",
        "--watch-json",
        help=
        "create or add to the watch list a json file to be used as configuration and data input for a schedule",
        nargs="+",
        default=[])
    PARSER.add_argument(
        "-s",
        "--start-queue",
        help=
        "start the queue process, updates data from the files in the watch list, then tweets based on the schedules",
        action="store_true")
    PARSER.add_argument(
        "-p",
        "--prune",
        help="remove orphan files from the watch list",
        action="store_true")
    PARSER.add_argument(
        "-r",
        "--repeat",
        help=
        "seconds to wait between queue processes, 300s default, use 0 or less to not repeat at all",
        default=300,
        type=int)
    ARGS = PARSER.parse_args()

    # TODO DANGEROUS code: All new options need to be here or they will be ignored
    if not ARGS.watch_json and not ARGS.start_queue and not ARGS.prune:
        PARSER.print_usage()
        PARSER.exit()

    # Frozen / not frozen, cxfreeze compatibility

    DIR = os.path.normpath(
        os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else __file__))
    os.chdir(DIR)  # The current dir should be the script home

    # Twitter tokens are needed

    try:
        TOKENS = json.load(open(TOKENS_FILE, 'r'))
    except (IOError, ValueError):

        TOKENS = {
            'example': {
                'consumer_key': "",
                'consumer_secret': "",
                'oauth_token': "",
                'oauth_secret': ""
            }
        }

    # Auto add to the token file an entry for each schedule, each one need to
    # have his own twitter account

    SCHEDS = DB.query(Schedule).all()
    for sc in SCHEDS:
        TOKENS[sc.name] = TOKENS.get(
            sc.name, {
                'consumer_key': "",
                'consumer_secret': "",
                'oauth_token': "",
                'oauth_secret': ""
            })

    with open(TOKENS_FILE, "w") as f:
        json.dump(TOKENS, f, indent=True)

    # Options

    if ARGS.prune:
        prune_watch_list()

    for jf in ARGS.watch_json:
        watch_json(jf)

    if ARGS.start_queue:

        # Thread to detect input commands and stop the repeat cycle

        REPEAT = True

        def stop_repeat():
            """
                Input detection thread.
            """
            global REPEAT
            while REPEAT:
                text = input()
                if text.strip().lower() == "q":  # Quit
                    REPEAT = False

        THREAD = threading.Thread(target=stop_repeat)
        THREAD.daemon = True
        THREAD.start()

        # Repeat cycle

        WAIT = 0
        COUNT = 1
        while REPEAT:

            process_queue(TOKENS)

            REPEAT = False if ARGS.repeat <= 0 else REPEAT
            if REPEAT:
                print()

            while REPEAT and WAIT < ARGS.repeat:
                sys.stdout.write(
                    f"\rWrite 'q' and press enter to quit ({ARGS.repeat - WAIT}s): "
                )
                sys.stdout.flush()

                WAIT += 1
                time.sleep(1)

            if REPEAT:
                WAIT = 0
                COUNT += 1
                print(f"\n\n#{COUNT}\n")

    print(f"\nAll done! ({round(time.time()-DELTA)}s)")
    time.sleep(2)
