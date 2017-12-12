""" Python Bot/library that queues tweets to post them later! """

import json
import os
import sys
import time
from datetime import datetime

import tweepy
from sqlalchemy import and_

from qdb import Post, Schedule, Time, init_database, sessionmaker

# Constants
TOKENS_FILE = "tokens.json"

# Database SQLAlchemy + SQLite
ENGINE = init_database()
SESSION = sessionmaker(bind=ENGINE)
DB = SESSION()


def update_schedule(name, days, hours):
    """ Create or update and return a schedule, assuming days as a list of
    numbers enumerating the days of the week (0-6) and hours a list of tuples of
    hours and minutes [(h m), ...]. """

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


def update_from_message(message):
    """ The message is a json file that contains all needed information for a
    working queue. The schedule will be created/updated, the messages will be
    queued, the tokens will be updated.

    qbot.json
    {
        "schedule": {
            "name": "example",
            "days": [
                "saturday",
                "sunday"
            ],
            "hours": [
                "10:00",
                "22:00"
            ],
            "twitter_tokens": {
                "consumer_key": "",
                "consumer_secret": "",
                "oauth_token": "",
                "oauth_secret": ""
            }
        },
        "messages": [
            {
                "text": "message #tag",
                "image": "c:/somewhere/image.gif"
            }
        ]
    } """

    try:
        message = json.load(open(message, 'r'))
    except (IOError, ValueError):
        print(f"The QBot message '{message}'\n"
              "Doesn't exists or isn't a valid json. Check it out.\n")
        return

    # Schedule

    schedule = message['schedule']['name']
    days = [get_int_day(i) for i in message['schedule']['days']]
    hours = [tuple(x.split(":")) for x in message['schedule']['hours']]

    update_schedule(schedule, days, hours)

    # Posts

    for post in message['messages']:
        queue_post(schedule, post['text'], post['image'])

    # Tokens

    try:
        tokens = json.load(open(TOKENS_FILE, 'r'))
    except (IOError, ValueError):
        tokens = {}

    tokens[schedule] = {
        'consumer_key':
        message['schedule']['twitter_tokens']['consumer_key'],
        'consumer_secret':
        message['schedule']['twitter_tokens']['consumer_secret'],
        'oauth_token':
        message['schedule']['twitter_tokens']['oauth_token'],
        'oauth_secret':
        message['schedule']['twitter_tokens']['oauth_secret']
    }

    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f)


def get_int_day(strday):
    """ Return the Schedule.day of the week assuming 'day' as an index from
    (0-6). """
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
    """ Return the Schedule.day of the week assuming 'day' as an index from
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


def process_queue(tokens):
    """ Tweet queued post based on the schedules. One at a time. """

    # What day are we?
    today = datetime.today()

    strday = str(get_schedule_column(today.weekday())).replace("Schedule.", "")
    print(f"Queue processing started\n"
          f"{strday.title()} {today.date()} {today.hour}:{today.minute:02}\n")

    # Get all the schedules for today
    todaysched = DB.query(Schedule).filter(
        get_schedule_column(today.weekday())).all()

    # Try to sed
    for tsc in todaysched:

        hour = DB.query(Time).filter(
            and_(Time.schedule_id == tsc.id, Time.used < today.date(),
                 Time.hour <= today.hour,
                 Time.minute <= today.minute)).first()

        print(f"Schedule '{tsc.name}'")

        if hour:

            print(f"At {hour.hour}:{hour.minute:02}")

            # Get the first unpublished post of the schedule in the hour
            post = DB.query(Post).filter(
                and_(Post.schedule_id == hour.schedule_id,
                     Post.published == 0)).first()

            if post:

                # Twitter auth and tokens validation

                auth = tweepy.OAuthHandler(tokens[tsc.name]['consumer_key'],
                                           tokens[tsc.name]['consumer_secret'])
                auth.set_access_token(tokens[tsc.name]['oauth_token'],
                                      tokens[tsc.name]['oauth_secret'])

                if not tokens[tsc.name]['consumer_key']:
                    print(
                        f"The schedule '{tsc.name}' need the Twitter account tokens.\n"
                        f"Write them in the 'tokens.json' and try again.\n")

                # Tweet

                else:

                    api = tweepy.API(
                        auth,
                        wait_on_rate_limit=True,
                        wait_on_rate_limit_notify=True)

                    if post.image_url:
                        api.update_with_media(post.image_url, post.text)
                    else:
                        api.update_status(post.text)

                    print(
                        f"Tweeted: {post.text} {post.image_url if not None else ''}\n"
                    )

                    # Mark the post as published, and register the hour used time

                    post.published = True
                    hour.used = datetime.now()

                    DB.add(hour)
                    DB.add(post)
                    DB.commit()

            else:
                print("The queue is empty!\n")

        else:
            print(f"No pending hours!\n")


if __name__ == "__main__":

    DELTA = time.time()

    # Frozen / not frozen, cxfreeze compatibility
    DIR = os.path.normpath(
        os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else __file__))
    os.chdir(DIR)

    # Twitter tokens are needed, one set by schedule

    try:
        TOKENS = json.load(open(TOKENS_FILE, 'r'))
    except (IOError, ValueError):

        TOKENS = {
            'default': {
                'consumer_key': "",
                'consumer_secret': "",
                'oauth_token': "",
                'oauth_secret': ""
            }
        }

        with open(TOKENS_FILE, "w") as f:
            json.dump(TOKENS, f)

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
        json.dump(TOKENS, f)

    # Do it

    print("QBot v0.1\n")
    # process_queue(TOKENS)
    update_from_message("qbot.json")
    print(f"All done! ({round(time.time()-DELTA)}s)")
