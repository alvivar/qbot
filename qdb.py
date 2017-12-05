""" Handles all qbot data using SQLAlchemy and sqlite. """

import os
import sys

from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Schedule(Base):
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


class Time(Base):
    __tablename__ = "time"
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    hour = Column(Integer)
    minute = Column(Integer)


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    schedule = relationship("Schedule")
    text = Column(String)
    image_url = Column(String)
    published = Column(Boolean, default=False)


def init_database():
    """ Create the database, return the engine. """
    engine = create_engine("sqlite:///data.db")
    Base.metadata.bind = engine
    Base.metadata.create_all()
    return engine


def update_schedule(db, name, days, hours):
    """ Create or update a schedule, assuming days as a list of numbers
    enumerating the days of the week (0-6) and hours a list of tuples of hours
    and minutes. """

    # Get
    schedule = db.query(Schedule).filter(Schedule.name == name).first()

    # Or create
    if schedule is None:
        schedule = Schedule()
        schedule.name = name
        db.add(schedule)
        db.flush()

    # Days of the week
    schedule.monday = True if 0 in days else False
    schedule.tuesday = True if 1 in days else False
    schedule.wednesday = True if 2 in days else False
    schedule.thursday = True if 3 in days else False
    schedule.friday = True if 4 in days else False
    schedule.saturday = True if 5 in days else False
    schedule.sunday = True if 6 in days else False

    # New hours
    db.query(Time).filter(Time.schedule_id == schedule.id).delete()
    for hm in hours:
        hour = Time()
        hour.hour = hm[0]
        hour.minute = hm[1]
        hour.schedule_id = schedule.id
        db.add(hour)

    # Save db
    db.add(schedule)
    db.commit()


def create_post(db, schedule_name, text, image_url):

    # Get
    schedule = db.query(Schedule).filter(
        Schedule.name == schedule_name).first()

    # Or create
    if schedule is None:
        schedule = Schedule()
        schedule.name = schedule_name

        db.add(schedule)
        db.flush()

    # New post
    post = Post()
    post.text = text
    post.image_url = image_url
    post.schedule_id = schedule.id

    db.add(post)
    db.commit()


if __name__ == "__main__":

    # Frozen / not frozen, cxfreeze compatibility
    DIR = os.path.normpath(
        os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else __file__))
    os.chdir(DIR)

    # Test

    ENGINE = init_database()
    SESSION = sessionmaker(bind=ENGINE)
    DB = SESSION()

    update_schedule(DB, "all days at 7", [0, 1, 2, 3, 4, 5, 6], [(7, 00),
                                                                 (19, 0)])
    update_schedule(DB, "weekend every 3 hours", [5, 6],
                    [(10, 00), (13, 00), (16, 00), (19, 00), (22, 00)])

    create_post(DB, "wthell", "is this even real?",
                r"C:\Users\matnesis\Documents\Overwatch\ScreenShots\Overwatch")
