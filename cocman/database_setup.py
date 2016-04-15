"""Database setup for the CoC Clan Manager project."""
from time import strftime
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
        tag (str): The Supercell assigned ID for the clan (globally unique).
        badge_url_medium (str): Medium sized clan badge graphic.
        badge_url_small (str): Small sized clan badge graphic.
        clan_level (int): The level of the clan.
        war_wins (int): Number of war wins the clan has achieved.
        war_win_streak (int): Number of war wins in a row.
        clan_points (int): The total points of the clan.
        required_trophies (int): Number of trophies required to join the clan.
        num_members (int): The number of members in the clan.
        members (Member): Member objects that are in this clan.
    """
    __tablename__ = 'clan'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    tag = Column(String(16), unique=True, nullable=False)
    badge_url_medium = Column(String(256))
    badge_url_small = Column(String(256))
    clan_level = Column(Integer)
    war_wins = Column(Integer)
    war_win_streak = Column(Integer)
    clan_points = Column(Integer)
    required_trophies = Column(Integer)
    num_members = Column(Integer)

    members = relationship('Member', cascade="save-update, merge, delete")

    @property
    def serialise(self):
        """Returns clan data in serialised format for JSON output."""
        return {
            'id': self.id,
            'name': self.name,
            'tag': self.tag,
            'badgeUrlMedium': self.badge_url_medium,
            'badgeUrlSmall': self.badge_url_small,
            'clanLevel': self.clan_level,
            'warWins': self.war_wins,
            'warWinStreak': self.war_win_streak,
            'clanPoints': self.clan_points,
            'requiredTrophies': self.required_trophies,
            'numMembers': self.num_members,
            'memberList' : [i.serialise for i in self.members]
        }


class Member(Base):
    """Define a database table of members, or players, of CoC.

    Attributes:
        __tablename__: A string naming the underlining SQL table.
        id (int): Internal ID number of the member.
        tag (str): Supercell assigned unique ID for a player in the game.
        name (str): Name of the member
        role (str): Type of member (e.g. member, admin (elder), coLeader,
            leader)
        exp_level (int): Experience level of the player.
        league_id (int): ID of the league the player is currently in this
            season.
        clan_rank (int): Current rank of the player within the clan.
        previous_clan_rank (int): Rank of the player 24 hours ago.
        current_donations (int): Number of troops donated by the player this
            season.
        current_donations_rec (int): Number of troops received this season.
        total_donations (int): Total number of troops donated.
        total_donations_rec (int): Total number of troops received.
        first_tracked_time (datetime): Time when a new member is added to DB.
        last_active_time (datetime): Time when a member was last active.
        clan_id (int): ID of the clan the player is a member of.
        clan (Clan): Makes a relationship between a member and a clan.
    """
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    tag = Column(String(16), unique=True, nullable=False)
    name = Column(String(64), nullable=False)
    role = Column(String(16), nullable=False)
    exp_level = Column(Integer, nullable=False)
    league_id = Column(Integer)
    league_name = Column(String(64))
    league_icon_tiny = Column(String(256))
    clan_rank = Column(Integer)
    previous_clan_rank = Column(Integer)
    current_donations = Column(Integer)
    current_donations_rec = Column(Integer)
    total_donations = Column(Integer)
    total_donations_rec = Column(Integer)
    first_tracked_time = Column(DateTime)
    last_active_time = Column(DateTime)

    clan_id = Column(Integer, ForeignKey('clan.id'))
    clan = relationship(Clan)

    @property
    def serialise(self):
        """Returns member data in serialised format for JSON output."""
        return {
            'id': self.id,
            'tag': self.tag,
            'name': self.name,
            'role': self.role,
            'expLevel': self.exp_level,
            'leagueId': self.league_id,
            'leagueName': self.league_name,
            'leagueIconTiny': self.league_icon_tiny,
            'clanRank': self.clan_rank,
            'previousClanRank': self.previous_clan_rank,
            'currentDonations': self.current_donations,
            'currentDonationsRec': self.current_donations_rec,
            'totalDonations': self.total_donations,
            'totalDonationsRec': self.total_donations_rec,
            'firstTrackedTime': self.first_tracked_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'lastActiveTime': self.last_active_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }


def create_db(database_url):
    """Create an empty database with the tables defined above."""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    # Create a Null Clan to store members that not in a tracked.
    from sqlalchemy import exists
    from cocman.connect_to_database import connect_to_database
    session = connect_to_database()
    (already_exists, ), = session.query(exists().where(Clan.tag == '#NULL'))

    if already_exists is False:
        null_clan = Clan(name='Null Clan', tag='#NULL')
        session.add(null_clan)
        session.commit()

    session.close()
