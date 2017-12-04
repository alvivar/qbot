""" Handles all qbot data. """

import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Schedule():
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    times = relationship("Time")
    name = Column(String)
    monday = Column(Boolean)
    tuesday = Column(Boolean)
    wednesday = Column(Boolean)
    thursday = Column(Boolean)
    friday = Column(Boolean)
    saturday = Column(Boolean)
    sunday = Column(Boolean)


class Time():
    __tablename__ = "time"
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    hour = Column(Integer)
    minute = Column(Integer)


class Post():
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


# def update_team(session, auth_response):
#     """ Create or update a team with his info and auth tokes. """

#     # Get
#     team = session.query(Team).filter(
#         Team.SlackId == auth_response["team_id"]).first()

#     # Create
#     if team is None:
#         team = Team()
#         team.SlackId = auth_response["team_id"]

#     team.AccessToken = auth_response['access_token']
#     team.BotAccessToken = auth_response['bot']['bot_access_token']

#     session.add(team)
#     session.commit()

if __name__ == "__main__":

    # Frozen / not frozen, cxfreeze compatibility
    DIR = os.path.normpath(
        os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else __file__))
    os.chdir(DIR)

    ENGINE = init_database()
    SESSION = sessionmaker(bind=ENGINE)
    DB = SESSION()

    # TEAM = Team(
    #     SlackId="SlackIdTest",
    #     AccessToken="AccessTokenTest",
    #     BotAccessToken="BotAccessTokenTest",
    #     Channel="ChannelTest")

    # DB.add(TEAM)
    # DB.commit()
