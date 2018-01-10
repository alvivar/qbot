"""
    Test file to see if everything works.
"""

import os
import sys

import qbot

if __name__ == "__main__":

    # Frozen / not frozen, cxfreeze compatibility
    DIR = os.path.normpath(
        os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else __file__))
    os.chdir(DIR)

    # Test

    qbot.update_schedule("week", [0, 1, 2, 3, 4, 5, 6], [(7, 00), (10, 00),
                                                         (13, 00)])
    qbot.update_schedule("weekend", [5, 6], [(10, 00), (13, 00), (16, 00),
                                             (19, 00), (22, 00)])

    qbot.queue_post("week", "this tweet is a text test (1) #ignore")

    qbot.queue_post("week", "this tweet is an image test (1) #ignore",
                    r"C:\Users\matnesis\Downloads\400.png")

    qbot.queue_post("week", "this tweet is a text test (2) #ignore")

    qbot.queue_post("week", "this tweet is an image test (2) #ignore",
                    r"C:\Users\matnesis\Downloads\444.png")

    # qbot.process_queue()
