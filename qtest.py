""" Test file to see if everything works. """

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

    qbot.update_schedule("all days at 7", [0, 1, 2, 3, 4, 5, 6], [(7, 00),
                                                                  (19, 0)])
    qbot.update_schedule("weekend every 3 hours", [5, 6],
                         [(10, 00), (13, 00), (16, 00), (19, 00), (22, 00)])

    qbot.create_post(
        "wthell", "is this even real?",
        r"C:\Users\matnesis\Documents\Overwatch\ScreenShots\Overwatch\lol.gif")

    qbot.process_queue()
