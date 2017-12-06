""" Handles all qbot data using SQLAlchemy and sqlite. """

import datetime
import os
import sys

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        and_, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

BASE = declarative_base()


class Schedule(BASE):
    """ Holds the schedule of publication, days and hours. """
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    times = relationship("Time")
    name = Column(String)
    monday = Column(Boolean, default=False)
    tuesday = Column(Boolean, default=False)
    wednesday = Column(Boolean, default=False)
    thursday = Column(Boolean, default=False)
    friday = Column(Boolean, default=False)
    saturday = Column(Boolean, default=False)
    sunday = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(
        DateTime,
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now)


class Time(BASE):
    """ Hours of publication in a Schedule. """
    __tablename__ = "time"
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    hour = Column(Integer)
    minute = Column(Integer)
    used = Column(DateTime, default=datetime.datetime(1984, 9, 11))
    created = Column(DateTime, default=datetime.datetime.now)


class Post(BASE):
    """ Posts to be published on Schedule time. """
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    schedule = relationship("Schedule")
    text = Column(String)
    image_url = Column(String)
    published = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(
        DateTime,
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now)


def init_database():
    """ Create the database, return the engine. """

    # The main dir should be the script dir
    currdir = os.path.normpath(
        os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else
            __file__))  # Frozen / not frozen, cxfreeze compatibility
    os.chdir(currdir)

    engine = create_engine("sqlite:///data.db")
    BASE.metadata.bind = engine
    BASE.metadata.create_all()

    return engine


if __name__ == "__main__":

    # Connection
    ENGINE = init_database()
    SESSION = sessionmaker(bind=ENGINE)
    DB = SESSION()
