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

    # Create or update clan details
    try:
        # Get clan object to be updated
        clan = session.query(Clan).filter_by(tag=clan_tag).one()
        clan.name = clan_data['name']
    except NoResultFound:
        # Create a new clan object
        clan = Clan(
            name=clan_data['name'],
            tag=clan_data['tag']
        )

    # Update optional data items
    clan.badge_url_medium = clan_data['badgeUrls']['medium']
    clan.badge_url_small = clan_data['badgeUrls']['small']

    # Commit the clan object to the database
    session.add(clan)
    session.commit()

    # Extract the members list data
    members_data = clan_data['memberList']

    # Loop through the current members of the clan
    for member_data in members_data:
        # Create or update member details
        try:
            # Get member object to be updated
            member = (session.query(Member)
                .filter_by(tag=member_data['tag']).one())

            # Update required fields
            member.name = member_data['name']
            member.role = member_data['role']
            member.exp_level = member_data['expLevel']

        except NoResultFound:
            # Create a new member object with required data
            member = Member(
                clan=clan,
                tag=member_data['tag'],
                name=member_data['name'],
                role=member_data['role'],
                exp_level=member_data['expLevel']
            )

        # Update optional member data
        member.league_id = member_data['league']['id']
        member.clan_rank = member_data['clanRank']
        member.previous_clan_rank = member_data['previousClanRank']

        # Update the current and total donations
        if member.current_donations:
            if member_data['donations'] != member.current_donations:
                # Number of donations has changed since last checked,
                # so update the last active time
                member.last_active_time = datetime.datetime.now()

                if member_data['donations'] < member.current_donations:
                    # At the end of the season, donation data is zeroed.
                    # Just add what we know now to the total donations.
                    member.total_donations += member_data['donations']
                else:
                    # Update the total donations
                    member.total_donations += (member_data['donations']
                        - member.current_donations)
        else:
            # This is the case of a new member we have no previous data for.
            member.total_donations = member_data['donations']

        # Update the current donations
        member.current_donations = member_data['donations']

        # Update the current and total donations received
        if member.current_donations_rec:
            if member_data['donationsReceived'] != member.current_donations_rec:
                # Number of donations has changed since last checked,
                # so update the last active time
                member.last_active_time = datetime.datetime.now()

                if (member_data['donationsReceived'] <
                    member.current_donations_rec):
                    # At the end of the season, donation data is zeroed.
                    # Just add what we know now to the total donations.
                    member.total_donations_rec += member_data[
                        'donationsReceived']
                else:
                    # Update the total donations
                    member.total_donations_rec += member_data[
                        'donationsReceived'] - member.current_donations_rec
        else:
            # This is the case of a new member we have no previous data for.
            member.total_donations_rec = member_data['donationsReceived']

        # Update the current donations
        member.current_donations_rec = member_data['donationsReceived']

        # TODO: Refactor the above two sections of code into a function

        # Commit the member object to the database
        session.add(member)
        session.commit()

    # Close the database session
    session.close()
