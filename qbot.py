""" Python Bot/library that queues tweets to post them later! """

import json
import os
import sys
import time
from enum import IntEnum

DAYS = IntEnum(
    "DAYS",
    "Monday Tuesday Wednesday Thursday Friday Saturday Sunday",
    start_at=0)


def set_schedule(name, *, days_list=None, times_list=None):
    pass


def queue_post(schedule_name, *, message=None, image=None):
    pass


def process_queue():
    pass


if __name__ == "__main__":

    DELTA = time.time()
    print("twqbot\n")

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
