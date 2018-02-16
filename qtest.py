"""
    Test file to see if everything works.
"""

import os
import sys

import qbot

if __name__ == "__main__":

    # HOME is the script directory + cx_Freeze compatibility
    HOME = os.path.normpath(
        os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else __file__))
    os.chdir(HOME)

    # Test

    qbot.update_schedule("test", [0, 1, 2, 3, 4, 5, 6], [(18, 20)])

    qbot.queue_post("test", "this tweet is a text test #ignore")

    qbot.process_queue()
