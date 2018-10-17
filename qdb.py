"""
    Handles all Qbot data using SQLAlchemy and sqlite.
"""

import datetime
import os
import sys

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy import Time as Time_
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

BASE = declarative_base()


class Schedule(BASE):
    """
        Holds the schedule of publication, days and hours.
    """

    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    times = relationship("Time")
    timers = relationship("Timer")
    name = Column(String)
    hours_enabled = Column(Boolean, default=False)
    timer_enabled = Column(Boolean, default=False)
    monday = Column(Boolean, default=False)
    tuesday = Column(Boolean, default=False)
    wednesday = Column(Boolean, default=False)
    thursday = Column(Boolean, default=False)
    friday = Column(Boolean, default=False)
    saturday = Column(Boolean, default=False)
    sunday = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime, onupdate=datetime.datetime.now,
                     default=datetime.datetime.now)


class Time(BASE):
    """
        Hours of publication in a Schedule.
    """

    __tablename__ = "time"
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    time = Column(Time_, default=datetime.time(0, 0))
    used = Column(DateTime, default=datetime.datetime(1984, 9, 11))
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime,
                     onupdate=datetime.datetime.now,
                     default=datetime.datetime.now)


class Timer(BASE):
    """
        Timer
    """

    __tablename__ = "timer"
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    hours = Column(Float, default=0)
    minutes = Column(Float, default=0)
    seconds = Column(Float, default=0)
    clocked = Column(Float, default=0)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime,
                     onupdate=datetime.datetime.now,
                     default=datetime.datetime.now)


class Post(BASE):
    """
        Posts to be published on Schedule time.
    """

    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    schedule = relationship("Schedule")
    text = Column(String)
    image_url = Column(String)
    published = Column(Boolean, default=False)
    error = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime,
                     onupdate=datetime.datetime.now,
                     default=datetime.datetime.now)


class Watch(BASE):
    """
        Folder paths to watch for qbot.json file messages.
    """

    __tablename__ = "watch"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime,
                     onupdate=datetime.datetime.now,
                     default=datetime.datetime.now)


def init_database():
    """
        Create the database, return the engine.
    """

    # The current dir should be the script home
    homedir = os.path.normpath(
        os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else
            __file__))  # cx_Freeze compatibility
    os.chdir(homedir)

    engine = create_engine("sqlite:///data.db")
    BASE.metadata.bind = engine
    BASE.metadata.create_all()

    return engine


if __name__ == "__main__":

    # Connection test
    ENGINE = init_database()
    SESSION = sessionmaker(bind=ENGINE)
    DB = SESSION()
