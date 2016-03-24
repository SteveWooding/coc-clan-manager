"""Update the database with data from the CoC API."""
import datetime

from sqlalchemy.orm.exc import NoResultFound

from coc.api import ClashOfClans

from cocman import app
from cocman.database_setup import Clan, Member
from cocman.connect_to_database import connect_to_database


def update_database(clan_tag):
    """Update the database with the given clan tag."""
    print "update_database() called..."
    # Connect to the database
    session = connect_to_database()

    # Get the clan data from the API
    coc_api = ClashOfClans(app.config['COC_API_KEY'])
    clan_data = coc_api.clans(clan_tag).get()

    # Should get a reponse code of 200, otherwise an error
    # occurred with the API request.
    if clan_data.status_code != 200:
        print "Error get data from API. Aborting..."
        return

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

        # Add this member to the current member tags list.
        current_member_tags.append(member_data['tag'])

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
        session.add(left_member)
        session.commit()

    # Close the database session
    session.close()
