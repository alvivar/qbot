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

    # qbot.update_schedule("week", [0, 1, 2, 3, 4, 5, 6], [(7, 00), (19, 0)])
    # qbot.update_schedule("weekend", [5, 6], [(10, 00), (13, 00), (16, 00),
    #                                          (19, 00), (22, 00)])

    # qbot.create_post("week", "hello deja el show",
    #                  r"https://dummyimage.com/400")

    # qbot.create_post("week", "podriamos querernos diferente",
    #                  r"https://dummyimage.com/400")

    # qbot.create_post("wthell", "is this even real?",
    #                  r"https://dummyimage.com/400")

    qbot.process_queue()
