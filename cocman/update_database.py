"""Update the database with data from the CoC API."""
import datetime

from sqlalchemy.orm.exc import NoResultFound

from coc.api import ClashOfClans

from cocman import app
from cocman.database_setup import Clan, Member
from cocman.connect_to_database import connect_to_database


def update_database(clan_tag):
    """Update the database with the given clan tag."""
    # Connect to the database
    session = connect_to_database()

    # Get the clan data from the API
    coc_api = ClashOfClans(app.config['COC_API_KEY'])
    clan_data = coc_api.clans(clan_tag).get()

    # Should get a reponse code of 200, otherwise an error
    # occurred with the API request.
    if clan_data.status_code != 200:
        print "Error getting data from API. Aborting..."
        return

    try:
        # Get clan object to be updated
        clan = session.query(Clan).filter_by(tag=clan_tag).one()
        clan.name = clan_data['name']
    except NoResultFound:
        # Create a new clan object
        clan = Clan(
            name=clan_data['name'],
            tag=clan_data['tag'],
            war_win_streak_high=0
        )

    # Update optional clan data items
    clan.badge_url_medium = clan_data['badgeUrls']['medium']
    clan.badge_url_small = clan_data['badgeUrls']['small']
    clan.clan_level = clan_data['clanLevel']
    clan.clan_points = clan_data['clanPoints']
    clan.num_members = clan_data['members']
    clan.war_wins = clan_data['warWins']
    clan.war_win_streak = clan_data['warWinStreak']
    clan.required_trophies = clan_data['requiredTrophies']

    # Update war ties and losses, if the clan has a public war log
    if clan_data['isWarLogPublic'] is True:
        clan.war_ties = clan_data['warTies']
        clan.war_losses = clan_data['warLosses']

    # Update war win streak all time record
    if clan_data['warWinStreak'] > clan.war_win_streak_high:
        clan.war_win_streak_high = clan_data['warWinStreak']

    # Commit the clan object to the database
    session.add(clan)
    session.commit()

    # Extract the members list data
    members_data = clan_data['memberList']

    # Empty list to store the current member tags for later
    # comparison with the database.
    current_member_tags = []

    # Loop through the current members of the clan
    for member_data in members_data:
        # Create or update member details
        try:
            # Get member object to be updated
            member = (session.query(Member)
                .filter_by(tag=member_data['tag']).one())

            # Check if the member was in another clan at the
            # time of the last API query.
            if member.clan_id != clan.id:
                # Move the member into this clan.
                member.clan = clan

            # Update required fields
            member.name = member_data['name']
            member.role = convert_role(member_data['role'])
            member.exp_level = member_data['expLevel']
            member.trophies = member_data['trophies']

        except NoResultFound:
            # Create a new member object with required data
            now = datetime.datetime.now()
            member = Member(
                clan=clan,
                tag=member_data['tag'],
                name=member_data['name'],
                role=convert_role(member_data['role']),
                exp_level=member_data['expLevel'],
                trophies=member_data['trophies'],
                first_tracked_time=now,
                last_active_time=now
            )

        # Update optional member data
        member.league_id = member_data['league']['id']
        member.league_name = member_data['league']['name']
        member.league_icon_tiny = member_data['league']['iconUrls']['tiny']
        member.clan_rank = member_data['clanRank']
        member.previous_clan_rank = member_data['previousClanRank']

        # Add this member to the current member tags list.
        current_member_tags.append(member_data['tag'])

        # Update member donations given and received
        update_member_stats(member, member_data['donations'], False)
        update_member_stats(member, member_data['donationsReceived'], True)

        # Commit the member object to the database
        session.add(member)
        session.commit()

    # Check if any members have left the clan. If so, move them to the Null Clan
    previous_member_tags = session.query(Member.tag).filter_by(clan=clan).all()
    previous_member_tags = set([tag for (tag,) in previous_member_tags])
    current_member_tags = set(current_member_tags)

    # Use sets to see who was previously in the clan and now is not.
    left_member_tags = list(previous_member_tags.difference(
        current_member_tags))

    # Move the missing members into the Null Clan
    null_clan = session.query(Clan).filter_by(tag='#NULL').one()
    for tag in left_member_tags:
        left_member = session.query(Member).filter_by(tag=tag).one()
        left_member.clan = null_clan
        left_member.clan_rank = 0
        left_member.previous_clan_rank = 0
        session.add(left_member)
        session.commit()

    # Close the database session
    session.close()


def convert_role(raw_role):
    """Convert the roles defined by the API to those used in the game."""
    roles = {'member': 'Member',
             'admin': 'Elder',
             'coLeader': 'Co-leader',
             'leader': 'Leader'}

    return roles[raw_role]


def update_member_stats(member, latest_num_donations, is_donations_rec):
    if is_donations_rec is True:
        current_donations_variable = 'current_donations_rec'
        total_donations_variable = 'total_donations_rec'
    else:
        current_donations_variable = 'current_donations'
        total_donations_variable = 'total_donations'

    member_current_donations = getattr(member, current_donations_variable)
    member_total_donations = getattr(member, total_donations_variable)

    if member_current_donations:
        if latest_num_donations > member_current_donations:
            # Update the last active date and total donations
            member.last_active_time = datetime.datetime.now()

            new_total_donations = (member_total_donations
                + (latest_num_donations - member_current_donations))

            setattr(member, total_donations_variable, new_total_donations)

        elif latest_num_donations < member_current_donations:
            # At the end of the season, donation data is zeroed.
            # Just add what we know now to the total donations.
            new_total_donations = member_total_donations + latest_num_donations
            setattr(member, total_donations_variable, new_total_donations)

            # Check for activity since the reset
            if latest_num_donations > 0:
                member.last_active_time = datetime.datetime.now()

    elif member_total_donations is None:
        # This is the case of a new member we have no previous data for, so
        # just initalise the total donations to the first new data we have.
        setattr(member, total_donations_variable, latest_num_donations)

    # Update the current donations
    setattr(member, current_donations_variable, latest_num_donations)
