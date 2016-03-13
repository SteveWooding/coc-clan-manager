"""Database setup for the CoC Clan Manager project."""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Get the base class mapper from SQLalchemy
Base = declarative_base()

class Clan(Base):
    """Define a database table of clans that a player belongs to.

    Attributes:
        __tablename__: A string naming the underlining SQL table.
        id (int): Internal ID number of the clan.
        name (str): Name of the clan.
        tag: The Supercell assigned ID for the clan (globally unique).
    """
    __tablename__ = 'clan'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    tag = Column(String(20), nullable=False)
    badge_url_medium = Column(String(256))
    badge_url_small = Column(String(256))
    members = relationship('Member', cascade="save-update, merge, delete")


class Member(Base):
    """Define a database table of members, or players, of CoC.

    Attributes:
        __tablename__: A string naming the underlining SQL table.
        id (int): Internal ID number of the member.
        name (str): Name of the member
        role (str): Type of member (e.g. member, admin (elder), coLeader, leader)
        exp_level (int): Experience level of the player.
        league_id (int): ID of the league the player is currently in this season.
        clan_rank (int): Current rank of the player within the clan.
        previous_clan_rank (int): Rank of the player 24 hours ago.
        current_donations (int): Number of troops donated by the player this season.
        current_donations_rec (int): Number of troops received this season.
        total_donations (int): Total number of troops donated.
        total_donations_rec (int): Total number of troops received.
        clan_id (int): ID of the clan the player is a member of.
        clan: Makes a relationship between a member and a clan.
    """
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    role = Column(String(8), nullable=False)
    exp_level = Column(Integer, nullable=False)
    league_id = Column(Integer)
    clan_rank = Column(Integer)
    previous_clan_rank = Column(Integer)
    current_donations = Column(Integer)
    current_donations_rec = Column(Integer)
    total_donations = Column(Integer)
    total_donations_rec = Column(Integer)
    last_active_time = Column(DateTime)

    clan_id = Column(Integer, ForeignKey('clan.id'))
    clan = relationship(Clan)


def create_db(database_url):
    """Create an empty database with the tables defined above."""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    print "Empty database created..."